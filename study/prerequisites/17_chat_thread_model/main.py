"""Dify 일반 Chat 앱의 스레드 모델 — "요청 스레드 = 소비자 / 워커 스레드 = 생산자" 구조를 축소 재현.

Dify 에서의 실제 흐름 (api/ 기준, chat / completion / agent-chat 공통)
  1) controllers/console/app/completion.py ChatMessageApi.post
       → services/app_generate_service.py → ChatAppGenerator.generate()
  2) core/app/apps/chat/app_generator.py : generate()
       - DB 에 Conversation / Message 레코드 생성 (_init_generate_records)
       - MessageBasedAppQueueManager 생성 (내부에 queue.Queue 하나)
       - contextvars.copy_context() + @copy_current_request_context 로 컨텍스트 복사
       - threading.Thread(target=worker_with_context).start()   ← LLM 호출은 이 워커 스레드에서
       - _handle_response() → EasyUIBasedGenerateTaskPipeline.process()  ← 요청 스레드는 큐를 소비
  3) 워커: _generate_worker()
       - with flask_app.app_context():  (스레드가 바뀌면 app context 가 없으므로 다시 push)
       - ChatAppRunner.run() → base_app_runner._handle_invoke_result_stream()
           LLM chunk 마다 queue_manager.publish(QueueLLMChunkEvent, APPLICATION_MANAGER)
           끝나면       queue_manager.publish(QueueMessageEndEvent, APPLICATION_MANAGER)
       - 예외는 잡아서 queue_manager.publish_error(e) 로 "큐에 실어" 요청 스레드에 전달
       - finally: db.session.close()  (스레드 로컬 세션 정리)
  4) core/app/apps/base_app_queue_manager.py : AppQueueManager
       - listen(): q.get(timeout=1) 루프. 1초마다 깨어나서
             · Redis stop flag 확인 → 있으면 QueueStopEvent publish
             · 10초마다 QueuePingEvent publish (SSE 연결 유지)
       - stop_listen(): q.put(None) → listen() 종료 신호
       - set_stop_flag(): Redis "generate_task_stopped:{task_id}" (다른 요청/다른 프로세스에서 호출)
  5) core/app/apps/message_based_app_queue_manager.py : _publish()
       - 종료 이벤트(MessageEnd / Stop / Error)면 stop_listen() 호출
       - publish_from == APPLICATION_MANAGER(=워커) 이고 stop flag 가 있으면
         GenerateTaskStoppedError 를 raise → 워커가 LLM 스트림 소비를 중단
  6) core/app/task_pipeline/easy_ui_based_generate_task_pipeline.py : _process_stream_response()
       - for message in queue_manager.listen(): 이벤트 → StreamResponse 변환 → SSE yield
  7) base_app_generator.convert_to_event_stream() → "data: {...}\\n\\n" / "event: ping\\n\\n"
  8) 중지 API: POST /apps/<id>/chat-messages/<task_id>/stop
       → AppTaskService.stop_task → AppQueueManager.set_stop_flag (Redis setex)
     ※ 중지 요청은 "다른 HTTP 요청"(다른 스레드, 심지어 다른 gunicorn 워커 프로세스)으로 들어오므로
       메모리 공유가 안 된다 → 그래서 Redis 플래그를 쓴다. 여기서는 TTL dict 로 흉내낸다.

  ┌─ 요청 스레드 (gunicorn/gevent worker) ─────────┐        ┌─ 워커 스레드 ───────────────────────┐
  │ generate()                                      │ start  │ _generate_worker()                  │
  │   queue_manager = QueueManager()  ──────────────┼───────▶│   with app.app_context():           │
  │   Thread(worker).start()                        │        │     for chunk in llm.stream():      │
  │   return SSE(pipeline(queue_manager.listen()))  │        │       publish(LLMChunk) ──┐         │
  │                                                 │        │     publish(MessageEnd)   │         │
  │ listen():  while True: q.get(timeout=1) ◀───────┼────────┼───────── queue.Queue ◀───┘         │
  │    ├ None 이면 종료                             │        │   except Exception as e:            │
  │    ├ 1초마다 stop flag 확인 → Stop publish      │        │     publish_error(e)                │
  │    └ 10초마다 Ping publish                      │        └─────────────────────────────────────┘
  └─────────────────────────────────────────────────┘                    ▲ GenerateTaskStoppedError
               ▲                                                         │ (publish 시 flag 확인)
               │ stop flag (Redis)  ◀── POST .../<task_id>/stop (다른 요청 스레드) ─┘

실행 (저장소 루트에서): uv run --project api python study/prerequisites/17_chat_thread_model/main.py
"""

import contextvars
import json
import logging
import queue
import sys
import threading
import time
import uuid
from collections.abc import Generator, Iterator, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

import httpx
from flask import (
    Flask,
    Response,
    copy_current_request_context,
    current_app,
    g,
    request,
    stream_with_context,
)
from httpx_sse import connect_sse
from werkzeug.serving import make_server

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(threadName)-22s] %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("demo")

app = Flask(__name__)

# 요청별 값을 담는 contextvar (Dify: core/app/... 의 trace / tenant 관련 contextvars 등)
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)

PING_INTERVAL = 3  # Dify 는 10초. 데모라 짧게.


# ---------------------------------------------------------------------------
# Redis 대용: TTL 이 있는 프로세스 공유 dict  (Dify: extensions.ext_redis.redis_client)
# ---------------------------------------------------------------------------
class FakeRedis:
    def __init__(self) -> None:
        self._data: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()

    def setex(self, key: str, ttl: int, value: str) -> None:
        with self._lock:
            self._data[key] = (value, time.monotonic() + ttl)

    def get(self, key: str) -> str | None:
        with self._lock:
            item = self._data.get(key)
            if item is None or item[1] < time.monotonic():
                return None
            return item[0]

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)


redis_client = FakeRedis()


# ---------------------------------------------------------------------------
# 이벤트 정의  (Dify: core/app/entities/queue_entities.py)
# ---------------------------------------------------------------------------
class PublishFrom(StrEnum):
    APPLICATION_MANAGER = "application_manager"  # 워커 스레드(Runner)가 publish
    TASK_PIPELINE = "task_pipeline"  # 요청 스레드(listen 루프)가 publish


@dataclass
class QueueEvent:
    pass


@dataclass
class QueueLLMChunkEvent(QueueEvent):
    text: str


@dataclass
class QueueMessageEndEvent(QueueEvent):
    total_tokens: int


@dataclass
class QueuePingEvent(QueueEvent):
    pass


@dataclass
class QueueStopEvent(QueueEvent):
    stopped_by: str = "user-manual"


@dataclass
class QueueErrorEvent(QueueEvent):
    error: Exception = field(default_factory=Exception)


@dataclass
class MessageQueueMessage:
    """큐에 실제로 들어가는 봉투. (Dify: MessageQueueMessage — task/message/conversation id 포함)"""

    task_id: str
    message_id: str
    conversation_id: str
    event: QueueEvent


class GenerateTaskStoppedError(Exception):
    """워커가 publish 하다가 stop flag 를 발견하면 던져서 LLM 루프를 빠져나온다."""


# ---------------------------------------------------------------------------
# AppQueueManager  (Dify: base_app_queue_manager.py + message_based_app_queue_manager.py)
# ---------------------------------------------------------------------------
class MessageBasedAppQueueManager:
    def __init__(
        self, task_id: str, user_id: str, conversation_id: str, message_id: str
    ) -> None:
        self._task_id = task_id
        self._user_id = user_id
        self._conversation_id = conversation_id
        self._message_id = message_id
        self._q: queue.Queue[MessageQueueMessage | None] = queue.Queue()
        # 이 task 의 소유자 기록 → stop 요청 시 본인 확인용 (Dify: generate_task_belong:{task_id}, TTL 1800)
        redis_client.setex(self._belong_key(task_id), 1800, user_id)

    # ---- 요청 스레드(소비자) ------------------------------------------------
    def listen(self) -> Iterator[MessageQueueMessage]:
        start = time.monotonic()
        last_ping = 0
        while True:
            try:
                message = self._q.get(timeout=1)  # 1초마다 반드시 깨어난다
                if message is None:  # stop_listen() 의 종료 신호
                    break
                yield message
            except queue.Empty:
                continue
            finally:
                # 메시지를 받았든 타임아웃이든 매번 실행: stop flag 확인 + ping
                elapsed = time.monotonic() - start
                if self._is_stopped():
                    self.publish(QueueStopEvent(), PublishFrom.TASK_PIPELINE)
                if elapsed // PING_INTERVAL > last_ping:
                    self.publish(QueuePingEvent(), PublishFrom.TASK_PIPELINE)
                    last_ping = int(elapsed // PING_INTERVAL)

    def stop_listen(self) -> None:
        redis_client.delete(self._belong_key(self._task_id))
        self._q.put(None)

    # ---- 양쪽 스레드 모두 호출 ---------------------------------------------
    def publish(self, event: QueueEvent, pub_from: PublishFrom) -> None:
        self._q.put(
            MessageQueueMessage(
                self._task_id, self._message_id, self._conversation_id, event
            )
        )

        if isinstance(event, QueueStopEvent | QueueErrorEvent | QueueMessageEndEvent):
            self.stop_listen()

        # 워커가 publish 하는 순간 stop flag 가 있으면 예외로 워커를 멈춘다
        if pub_from == PublishFrom.APPLICATION_MANAGER and self._is_stopped():
            raise GenerateTaskStoppedError()

    def publish_error(self, e: Exception, pub_from: PublishFrom) -> None:
        self.publish(QueueErrorEvent(error=e), pub_from)

    # ---- stop flag (다른 요청에서 설정) -------------------------------------
    def _is_stopped(self) -> bool:
        return redis_client.get(self._stopped_key(self._task_id)) is not None

    @classmethod
    def set_stop_flag(cls, task_id: str, user_id: str) -> bool:
        owner = redis_client.get(cls._belong_key(task_id))
        if owner != user_id:  # 남의 task 는 못 멈춘다 / 이미 끝난 task
            return False
        redis_client.setex(cls._stopped_key(task_id), 600, "1")
        return True

    @staticmethod
    def _belong_key(task_id: str) -> str:
        return f"generate_task_belong:{task_id}"

    @staticmethod
    def _stopped_key(task_id: str) -> str:
        return f"generate_task_stopped:{task_id}"


# ---------------------------------------------------------------------------
# Runner — 워커 스레드에서 LLM 을 호출 (Dify: ChatAppRunner + base_app_runner)
# ---------------------------------------------------------------------------
def fake_llm_stream(query: str) -> Iterator[str]:
    if "error" in query:
        yield "잠시만요"
        raise ValueError("model provider rate limited (가짜 오류)")
    for token in [
        "'",
        query,
        "'",
        " 에 ",
        "대해 ",
        "천천히 ",
        "답변을 ",
        "생성하는 ",
        "중입니다",
        ".",
    ]:
        time.sleep(0.4)  # LLM 이 느리다
        yield token


class ChatAppRunner:
    def run(self, query: str, queue_manager: MessageBasedAppQueueManager) -> None:
        tokens = 0
        for chunk in fake_llm_stream(query):
            tokens += 1
            log.info("worker  publish chunk %r", chunk)
            queue_manager.publish(
                QueueLLMChunkEvent(chunk), PublishFrom.APPLICATION_MANAGER
            )
        queue_manager.publish(
            QueueMessageEndEvent(total_tokens=tokens), PublishFrom.APPLICATION_MANAGER
        )


# ---------------------------------------------------------------------------
# Generator — 스레드를 만들고 요청 스레드는 파이프라인으로 돌아간다 (Dify: ChatAppGenerator)
# ---------------------------------------------------------------------------
class ChatAppGenerator:
    def generate(self, query: str, user_id: str) -> Generator[Mapping[str, Any] | str]:
        task_id = str(uuid.uuid4())
        conversation_id, message_id = (
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        )  # 실제론 DB insert 결과
        queue_manager = MessageBasedAppQueueManager(
            task_id, user_id, conversation_id, message_id
        )

        context = contextvars.copy_context()  # ① contextvars 스냅샷

        @copy_current_request_context  # ② Flask request context 도 워커에서 쓸 수 있게
        def worker_with_context() -> None:
            context.run(
                self._generate_worker,
                flask_app=current_app._get_current_object(),  # type: ignore[attr-defined]
                query=query,
                queue_manager=queue_manager,
            )

        threading.Thread(
            target=worker_with_context, name=f"worker-{task_id[:8]}"
        ).start()
        log.info("request started worker thread, task_id=%s", task_id)

        # ③ 요청 스레드는 즉시 "큐 소비 파이프라인" 제너레이터를 반환 → SSE 로 흘러간다
        return self._process_stream_response(
            queue_manager, task_id, message_id, conversation_id
        )

    def _generate_worker(
        self, flask_app: Flask, query: str, queue_manager: MessageBasedAppQueueManager
    ) -> None:
        with (
            flask_app.app_context()
        ):  # ④ 새 스레드에는 app context 가 없으므로 직접 push
            # 주의: app_context() 를 새로 push 하면 g 는 "새 객체"가 된다 → 요청 스레드의 g.user_id 는 안 보임.
            #       그래서 Dify 는 user_id 등 필요한 값을 application_generate_entity 에 담아 인자로 넘긴다.
            log.info(
                "worker  started: request_id(contextvar)=%s, request.path=%s, g.user_id=%s",
                request_id_var.get(),  # contextvars.copy_context() 덕분에 보임
                request.path,  # @copy_current_request_context 덕분에 보임
                g.get("user_id"),  # None
            )
            try:
                ChatAppRunner().run(query, queue_manager)
            except GenerateTaskStoppedError:
                log.info("worker  stopped by stop flag → LLM 루프 탈출")
            # ⑤ 예외는 스레드 밖으로 못 나가므로 큐에 실어 보낸다 (Dify 도 Exception 을 잡아 publish_error)
            except Exception as e:  # noqa: BLE001
                log.info("worker  caught %r → publish_error", e)
                queue_manager.publish_error(e, PublishFrom.APPLICATION_MANAGER)
            finally:
                log.info("worker  finished (Dify 는 여기서 db.session.close())")

    def _process_stream_response(
        self,
        queue_manager: MessageBasedAppQueueManager,
        task_id: str,
        message_id: str,
        conversation_id: str,
    ) -> Generator[Mapping[str, Any] | str]:
        """Dify: EasyUIBasedGenerateTaskPipeline._process_stream_response — 큐 이벤트 → 스트림 응답."""
        answer = ""
        base = {
            "task_id": task_id,
            "message_id": message_id,
            "conversation_id": conversation_id,
        }
        for message in queue_manager.listen():
            match message.event:
                case QueueLLMChunkEvent(text=text):
                    answer += text
                    yield {"event": "message", **base, "answer": text}
                case QueuePingEvent():
                    yield "ping"
                case QueueErrorEvent(error=err):
                    yield {"event": "error", **base, "message": str(err)}
                    break
                case QueueStopEvent() | QueueMessageEndEvent():
                    # Dify: 여기서 _save_message() 로 지금까지의 answer 를 DB 에 저장
                    log.info("request pipeline end, save answer=%r", answer)
                    yield {
                        "event": "message_end",
                        **base,
                        "stopped": isinstance(message.event, QueueStopEvent),
                    }
                    break


def convert_to_event_stream(
    generator: Generator[Mapping[str, Any] | str],
) -> Generator[str]:
    for message in generator:
        if isinstance(message, Mapping):
            yield f"data: {json.dumps(message, ensure_ascii=False)}\n\n"
        else:
            yield f"event: {message}\n\n"


# ---------------------------------------------------------------------------
# Controllers
# ---------------------------------------------------------------------------
@app.before_request
def load_user() -> None:
    g.user_id = request.headers.get(
        "X-User", "anonymous"
    )  # Dify: flask_login current_user
    request_id_var.set(request.headers.get("X-Request-Id", str(uuid.uuid4())[:8]))


@app.post("/chat-messages")
def chat_messages() -> Response:
    body = request.get_json()
    stream = ChatAppGenerator().generate(body["query"], g.user_id)
    return Response(
        stream_with_context(convert_to_event_stream(stream)),
        mimetype="text/event-stream",
    )


@app.post("/chat-messages/<task_id>/stop")
def stop(task_id: str) -> dict[str, str]:
    accepted = MessageBasedAppQueueManager.set_stop_flag(task_id, g.user_id)
    log.info(
        "request stop task=%s user=%s accepted=%s", task_id[:8], g.user_id, accepted
    )
    return {"result": "success" if accepted else "ignored"}


# ---------------------------------------------------------------------------
# 데모 클라이언트
# ---------------------------------------------------------------------------
BASE = "http://127.0.0.1:5217"


def consume(
    query: str,
    user: str = "alice",
    stop_after: int | None = None,
    stop_as: str | None = None,
) -> None:
    headers = {"X-User": user, "X-Request-Id": f"req-{query.replace(' ', '-')}"}
    with (
        httpx.Client(timeout=30) as client,
        connect_sse(
            client,
            "POST",
            f"{BASE}/chat-messages",
            json={"query": query},
            headers=headers,
        ) as es,
    ):
        n = 0
        for sse in es.iter_sse():
            if sse.event == "ping":
                print("   client <- [ping]")
                continue
            data = sse.json()
            print(
                f"   client <- [{data['event']}] {data.get('answer') or data.get('message') or ''}"
                f"{' stopped=' + str(data['stopped']) if 'stopped' in data else ''}"
            )
            if data["event"] == "message":
                n += 1
                if stop_after is not None and n == stop_after:
                    # 별도 HTTP 요청(= 서버의 다른 요청 스레드)으로 중지
                    who = stop_as or user
                    r = client.post(
                        f"{BASE}/chat-messages/{data['task_id']}/stop",
                        headers={"X-User": who},
                    )
                    print(f"   client -> stop as {who}: {r.json()}")


def main() -> None:
    sys.stdout.reconfigure(
        line_buffering=True
    )  # 서버 로그와 클라이언트 출력 순서를 맞춘다
    server = make_server(
        "127.0.0.1", 5217, app, threaded=True
    )  # 요청마다 스레드 (gevent 대용)
    threading.Thread(
        target=server.serve_forever, name="http-server", daemon=True
    ).start()
    try:
        print(
            "\n== 1) 정상 흐름: 워커가 chunk publish → 요청 스레드가 listen() 으로 SSE 전송 (ping 포함) =="
        )
        consume("dify n8n archestra")

        print(
            "\n== 2) 중지: 3번째 chunk 후 /stop → stop flag → listen() 이 Stop publish, 워커는 예외로 탈출 =="
        )
        consume("stop me", stop_after=3)
        time.sleep(1)  # 워커 스레드 종료 로그 확인용

        print(
            "\n== 3) 다른 사용자의 stop 요청은 무시된다 (generate_task_belong 확인) =="
        )
        consume("other user", stop_after=2, stop_as="mallory")

        print(
            "\n== 4) 워커 예외: 스레드 안에서 잡아 QueueErrorEvent 로 전달 → SSE error 이벤트 =="
        )
        consume("error please")
        time.sleep(0.5)
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
