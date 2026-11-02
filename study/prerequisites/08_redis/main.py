"""Redis (redis-py) 예제 — 캐시 / 분산 락 / Rate Limit / Pub-Sub / Streams.

Dify 에서의 용도
  - api/extensions/ext_redis.py : 전역 `redis_client` (standalone / Sentinel / Cluster 지원 래퍼)
  - 캐시:        redis_client.setex(key, ttl, value)  — 토큰, 설정, 모델 자격증명 캐시 등
  - 분산 락:     with redis_client.lock(key, timeout=..)  — services/api_token_service.py 등
  - Rate limit:  libs/helper.py RateLimiter — ZSET + Lua 스크립트로 sliding window
  - 이벤트 전달: libs/broadcast_channel/redis/*  — Pub/Sub, Sharded Pub/Sub, Streams 구현.
                 Celery worker 에서 돌아가는 앱/워크플로 실행 이벤트를 API 프로세스의 SSE 응답으로 전달
                 (core/app/apps/streaming_utils.py, message_based_app_generator.py)
  - Celery 브로커/결과 백엔드 (09 예제)

준비: 로컬 개발용 middleware 의 redis (docker/docker-compose.middleware.yaml, 비밀번호 difyai123456)
      없으면: docker run -d -p 6379:6379 redis:6-alpine redis-server --requirepass difyai123456
실행: uv run --project api python example/08_redis/main.py
      (Dify 데이터와 섞이지 않게 기본으로 DB 15 사용, REDIS_URL 환경변수로 변경 가능)
"""

import os
import threading
import time
import uuid

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://:difyai123456@localhost:6379/15")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
PREFIX = "example:"


def demo_cache() -> None:
    print("== 1) 캐시 (SETEX / GET / TTL) ==")
    key = PREFIX + "model_credentials:tenant1"
    cached = r.get(key)
    if cached is None:
        print("cache miss → DB 조회 후 저장")
        r.setex(key, 5, '{"api_key": "sk-***"}')
    print("값:", r.get(key), "| TTL:", r.ttl(key), "초")


def demo_lock() -> None:
    print("\n== 2) 분산 락 (여러 프로세스/파드가 동시에 같은 작업을 하지 않도록) ==")
    lock_key = PREFIX + "lock:update_api_token_last_used"
    results: list[str] = []

    def worker(name: str) -> None:
        lock = r.lock(lock_key, timeout=10, blocking_timeout=0.2)
        if lock.acquire():
            try:
                results.append(f"{name}: 락 획득 → 작업 수행")
                time.sleep(0.5)
            finally:
                lock.release()
        else:
            results.append(f"{name}: 락 획득 실패 → skip")

    threads = [threading.Thread(target=worker, args=(f"worker-{i}",)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("\n".join(sorted(results)))


def demo_rate_limit() -> None:
    print("\n== 3) Rate Limit (ZSET sliding window + Lua, libs/helper.py RateLimiter) ==")
    script = r.register_script(
        """
        redis.call('ZREMRANGEBYSCORE', KEYS[1], '-inf', ARGV[1] - ARGV[2])
        if redis.call('ZCARD', KEYS[1]) >= tonumber(ARGV[3]) then return 0 end
        redis.call('ZADD', KEYS[1], ARGV[1], ARGV[4])
        redis.call('EXPIRE', KEYS[1], ARGV[2] * 2)
        return 1
        """
    )
    key = PREFIX + "email_code_rate_limit:user@example.com"
    r.delete(key)
    for i in range(5):
        ok = script(keys=[key], args=[int(time.time()), 60, 3, uuid.uuid4().hex])  # 60초에 3회
        print(f"메일 발송 요청 {i + 1}:", "허용" if ok else "차단 (too many requests)")


def demo_pubsub() -> None:
    print("\n== 4) Pub/Sub (fire-and-forget 브로드캐스트) ==")
    channel = PREFIX + "workflow_run:run-123"
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    pubsub.get_message(timeout=1)  # subscribe 확인 메시지 소비

    def publisher() -> None:
        for ev in ["node_started", "text_chunk", "node_finished", "workflow_finished"]:
            r.publish(channel, ev)
            time.sleep(0.05)

    threading.Thread(target=publisher).start()
    received = []
    while len(received) < 4:
        msg = pubsub.get_message(timeout=1)
        if msg and msg["type"] == "message":
            received.append(msg["data"])
    print("구독자가 받은 이벤트:", received)
    pubsub.close()


def demo_streams() -> None:
    print("\n== 5) Streams (영속 로그 — 늦게 붙은 소비자도 처음부터 다시 읽을 수 있음) ==")
    stream = PREFIX + "stream:workflow_run:run-456"
    r.delete(stream)
    for i, ev in enumerate(["workflow_started", "node_started", "node_finished", "workflow_finished"]):
        r.xadd(stream, {"event": ev, "seq": i}, maxlen=1000)
    # 클라이언트가 SSE 재연결 시 "마지막으로 받은 id 이후"부터 다시 읽는 구조
    entries = r.xrange(stream)
    last_seen = entries[1][0]
    print("전체:", [e[1]["event"] for e in entries])
    print(f"id {last_seen} 이후부터 재개:", [e[1]["event"] for e in r.xread({stream: last_seen})[0][1]])


def demo_pipeline() -> None:
    print("\n== 6) Pipeline (여러 명령을 한 번의 왕복으로) ==")
    with r.pipeline() as pipe:
        for i in range(3):
            pipe.incr(PREFIX + "counter")
        pipe.expire(PREFIX + "counter", 30)
        print("결과:", pipe.execute())


def main() -> None:
    try:
        r.ping()
    except redis.exceptions.RedisError as e:
        raise SystemExit(f"Redis 연결 실패 ({REDIS_URL}): {e}\n docstring 의 '준비' 항목을 참고하세요.")
    try:
        demo_cache()
        demo_lock()
        demo_rate_limit()
        demo_pubsub()
        demo_streams()
        demo_pipeline()
    finally:
        keys = list(r.scan_iter(PREFIX + "*"))
        if keys:
            r.delete(*keys)


if __name__ == "__main__":
    main()
