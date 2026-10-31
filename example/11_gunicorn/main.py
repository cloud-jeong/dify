"""Gunicorn 예제 — sync 워커 vs gevent 워커 비교.

Dify 에서의 용도 (api/docker/entrypoint.sh, MODE=api)
  gunicorn --bind 0.0.0.0:5001 \
           --workers ${SERVER_WORKER_AMOUNT:-1} \
           --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
           --worker-connections ${SERVER_WORKER_CONNECTIONS:-10} \
           --timeout ${GUNICORN_TIMEOUT:-200} \
           app:socketio_app
  - workers            : 프로세스 수 (CPU 코어 수 기준)
  - worker-class       : gevent + WebSocket 지원 워커 (Socket.IO 를 같은 포트에서 처리)
  - worker-connections : 워커 1개가 동시에 처리하는 greenlet(연결) 수
  - timeout            : 긴 LLM 스트리밍 응답 때문에 넉넉히 200초
  (DEBUG=true 이면 gunicorn 대신 `python -m app` 개발 서버로 실행)

이 예제는 같은 앱을 두 가지 워커로 띄우고, 1초짜리 요청 8개를 동시에 보내 걸린 시간을 비교한다.
실행: uv run --project api python example/11_gunicorn/main.py
"""

import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

HERE = Path(__file__).parent


def run(worker_class: str, port: int, extra: list[str]) -> None:
    cmd = [
        sys.executable, "-m", "gunicorn",
        "-c", str(HERE / "gunicorn.conf.py"),
        "--chdir", str(HERE),
        "--bind", f"127.0.0.1:{port}",
        "--workers", "1",
        "--worker-class", worker_class,
        *extra,
        "wsgi:app",
    ]  # fmt: skip
    proc = subprocess.Popen(cmd)
    try:
        for _ in range(50):  # 기동 대기
            try:
                httpx.get(f"http://127.0.0.1:{port}/slow", timeout=5)
                break
            except httpx.TransportError:
                time.sleep(0.2)

        start = time.perf_counter()
        with ThreadPoolExecutor(8) as ex:
            pids = list(
                ex.map(lambda _: httpx.get(f"http://127.0.0.1:{port}/slow", timeout=30).json()["pid"], range(8))
            )
        elapsed = time.perf_counter() - start
        print(f"{worker_class:<55} 요청 8개 → {elapsed:.2f}초 (처리한 워커 pid: {set(pids)})")
    finally:
        proc.terminate()
        proc.wait()


def main() -> None:
    run("sync", 5101, [])  # 워커 1개가 한 번에 1요청 → 약 8초
    run("gevent", 5102, ["--worker-connections", "100"])  # greenlet 으로 동시 처리 → 약 1초
    run("geventwebsocket.gunicorn.workers.GeventWebSocketWorker", 5103, ["--worker-connections", "100"])  # Dify 기본값


if __name__ == "__main__":
    main()
