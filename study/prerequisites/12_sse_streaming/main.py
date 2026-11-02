"""SSE(Server-Sent Events) 스트리밍 예제 — 서버(Flask) + 클라이언트(httpx-sse).

Dify 에서의 용도
  - 채팅/워크플로 실행 API 의 response_mode="streaming" 응답
      core/app/apps/base_app_generator.py : convert_to_event_stream()
          dict  → "data: {json}\n\n"
          str   → "event: ping\n\n"    (연결 유지용 ping)
      libs/helper.py : compact_generate_response() → Response(generator, mimetype="text/event-stream")
                       + stream_with_context 로 요청 컨텍스트 유지
  - 이벤트 종류 예: message, message_end, workflow_started, node_started, node_finished, workflow_finished, error
  - 클라이언트 측: 프론트엔드는 web/service/base.ts 의 ssePost,
    백엔드가 외부 SSE 를 소비할 때는 httpx-sse (core/mcp/client/sse_client.py, streamable_client.py — MCP 서버 연동)

실행: uv run --project api python example/12_sse_streaming/main.py
"""

import json
import logging
import threading
import time
import uuid
from collections.abc import Generator, Mapping

import httpx
from flask import Flask, Response, request, stream_with_context
from httpx_sse import connect_sse
from werkzeug.serving import make_server

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.WARNING)  # 접근 로그 숨김


def convert_to_event_stream(generator: Generator[Mapping | str]) -> Generator[str]:
    for message in generator:
        if isinstance(message, Mapping):
            yield f"data: {json.dumps(message, ensure_ascii=False)}\n\n"
        else:
            yield f"event: {message}\n\n"


def fake_chat_generator(query: str) -> Generator[Mapping | str]:
    """LLM 이 토큰 단위로 답변을 내보내는 상황을 흉내낸다."""
    message_id = str(uuid.uuid4())
    yield "ping"
    for token in ["안녕하세요", "! ", "'", query, "'", "에 ", "대해 ", "답변", "드릴게요."]:
        time.sleep(0.1)
        yield {"event": "message", "message_id": message_id, "answer": token}
    yield {"event": "message_end", "message_id": message_id, "metadata": {"usage": {"total_tokens": 42}}}


@app.post("/v1/chat-messages")
def chat_messages():
    body = request.get_json()
    if body.get("response_mode") == "blocking":
        answer = "".join(
            m["answer"] for m in fake_chat_generator(body["query"]) if isinstance(m, Mapping) and "answer" in m
        )
        return {"event": "message", "answer": answer}

    stream = convert_to_event_stream(fake_chat_generator(body["query"]))
    return Response(stream_with_context(stream), mimetype="text/event-stream")


def main() -> None:
    server = make_server("127.0.0.1", 5199, app, threaded=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:5199/v1/chat-messages"

    try:
        print("== 1) raw 스트림 (wire 포맷 그대로) ==")
        with httpx.stream("POST", url, json={"query": "SSE", "response_mode": "streaming"}) as resp:
            for i, line in enumerate(resp.iter_lines()):
                if line:
                    print("  ", line)
                if i > 6:
                    print("   ...")
                    break

        print("\n== 2) httpx-sse 로 이벤트 단위 파싱 ==")
        answer = ""
        with (
            httpx.Client() as client,
            connect_sse(client, "POST", url, json={"query": "Dify", "response_mode": "streaming"}) as es,
        ):
            for sse in es.iter_sse():
                if sse.event != "message":  # "event: ping" 줄
                    print(f"  [{sse.event}]")
                    continue
                data = sse.json()
                if data["event"] == "message":
                    answer += data["answer"]
                    print(f"  [message] +{data['answer']!r:<12} 누적: {answer}")
                elif data["event"] == "message_end":
                    print(f"  [message_end] usage={data['metadata']['usage']}")

        print("\n== 3) blocking 모드 ==")
        print("  ", httpx.post(url, json={"query": "blocking", "response_mode": "blocking"}).json())
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
