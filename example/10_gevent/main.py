"""gevent 예제 — 협력적 멀티태스킹(greenlet)과 monkey patching.

Dify 에서의 용도
  - API 서버: gunicorn 의 gevent 워커(GeventWebSocketWorker) 로 실행 → 하나의 프로세스가
    수백 개의 동시 요청(LLM 스트리밍처럼 오래 열려 있는 I/O 대기 요청)을 처리한다. (11 예제)
  - Celery worker: `-P gevent` 풀 (WORKER_POOL 기본값)
  - monkey patch 후 추가 패치가 필요한 라이브러리:
      api/gunicorn.conf.py      : GeventDidPatchBuiltinModulesEvent 구독 → grpc, psycopg2(psycogreen) 패치
      api/celery_entrypoint.py  : 같은 패치를 Celery 진입점에서 수행
      api/extensions/ext_database.py : gevent 환경에서 커넥션 풀 reset 시 안전한 rollback 처리
  - 주의: monkey.patch_all() 은 다른 모듈(socket, ssl, threading 을 쓰는 것)을 import 하기 "전에" 해야 한다.

실행: uv run --project api python example/10_gevent/main.py
"""

from gevent import monkey

monkey.patch_all()  # 반드시 가장 먼저! (표준 socket/time/threading 을 gevent 협력형 버전으로 교체)

import socket
import threading
import time

import gevent
from gevent.pool import Pool
from gevent.queue import Queue


def fake_llm_call(i: int) -> str:
    # time.sleep 은 patch 되어 gevent.sleep 과 같아짐 → 대기 동안 다른 greenlet 으로 전환
    time.sleep(1)
    return f"answer-{i}"


def demo_concurrency() -> None:
    print("== 1) 1초 걸리는 I/O 작업 10개 ==")
    start = time.perf_counter()
    jobs = [gevent.spawn(fake_llm_call, i) for i in range(10)]
    gevent.joinall(jobs)
    print(f"결과 {[j.value for j in jobs][:3]}... | 총 {time.perf_counter() - start:.2f}초 (순차라면 10초)")


def demo_pool() -> None:
    print("\n== 2) Pool 로 동시성 제한 (worker-connections 개념과 유사) ==")
    pool = Pool(3)
    start = time.perf_counter()
    results = pool.map(fake_llm_call, range(6))
    print(f"동시 3개 제한 → 6개 작업 {time.perf_counter() - start:.2f}초, {results}")


def demo_patched_stdlib() -> None:
    print("\n== 3) monkey patch 확인 ==")
    print("socket.socket       :", socket.socket)
    print("threading.Thread    :", threading.Thread)
    print("patched(socket)?    :", monkey.is_module_patched("socket"))
    # threading.Thread 도 사실 greenlet 위에서 돈다 → 진짜 OS 스레드가 아님
    t = threading.Thread(target=lambda: print("thread body runs in greenlet:", gevent.getcurrent()))
    t.start()
    t.join()


def demo_cpu_bound_blocks() -> None:
    print("\n== 4) 주의: CPU 바운드 작업은 다른 greenlet 을 막는다 ==")
    ticks: list[float] = []
    start = time.perf_counter()

    def ticker():
        for _ in range(3):
            ticks.append(round(time.perf_counter() - start, 2))
            gevent.sleep(0.1)

    def cpu_heavy():
        sum(i * i for i in range(8_000_000))  # 양보 지점이 없음

    gevent.joinall([gevent.spawn(ticker), gevent.spawn(cpu_heavy)])
    print("ticker 가 기록한 시각:", ticks, "← cpu_heavy 동안 멈췄다가 재개됨")
    print("→ 무거운 연산은 API(gevent) 프로세스가 아니라 별도 Celery worker 에서 돌리는 편이 안전하다")


def demo_queue() -> None:
    print("\n== 5) gevent.queue: greenlet 간 생산자/소비자 (스트리밍 응답 파이프라인과 유사) ==")
    q: Queue = Queue()

    def producer():
        for token in ["Hel", "lo", ", ", "Dify", "!"]:
            q.put(token)
            gevent.sleep(0.05)
        q.put(StopIteration)

    gevent.spawn(producer)
    print("consumer:", "".join(iter(q.get, StopIteration)))


if __name__ == "__main__":
    demo_concurrency()
    demo_pool()
    demo_patched_stdlib()
    demo_cpu_bound_blocks()
    demo_queue()
