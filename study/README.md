# Dify API 기술 스택 학습용 예제

`api/`(Dify 백엔드)에서 쓰는 핵심 기술을 하나씩 떼어내 **단독 실행 가능한 작은 프로그램**으로 만든 예제 모음입니다.
각 파일 상단 docstring 에 _"Dify 에서는 어디서 어떻게 쓰는지"_ 실제 코드 경로를 적어 두었으니, 예제를 돌려본 뒤 해당 파일을 열어 비교해 보세요.

## 실행 방법

별도 설치 없이 `api/` 의 가상환경(uv)을 그대로 사용합니다. **저장소 루트**에서:

```bash
uv run --project api python example/01_pydantic/main.py
```

Redis 가 필요한 예제(08, 09, 13 `--redis`)는 로컬 개발용 middleware 의 Redis 를 사용합니다.

```bash
# 안 떠 있다면 (docker/ 디렉터리에서)
docker compose -f docker-compose.middleware.yaml up -d redis ssrf_proxy
# 기본 접속 URL: redis://:difyai123456@localhost:6379/15  (Dify 데이터와 분리하려고 DB 15 사용)
# 다르면 REDIS_URL 환경변수로 지정
```

## 예제 목록

| #   | 기술                                  | 보여주는 것                                                                      | Dify 의 실제 위치                                                        | 외부 의존         |
| --- | ------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------- |
| 01  | **Pydantic v2 / pydantic-settings**   | 환경변수 → 타입 검증된 설정, 다중 상속 설정 합성, 요청 payload 검증, JSON Schema | `configs/app_config.py`, `controllers/**`                                | -                 |
| 02  | **Flask App Factory**                 | `create_app()`, `ext_*.init_app()` 순차 초기화, Blueprint, 공통 에러 핸들러      | `app_factory.py`, `extensions/ext_*.py`                                  | -                 |
| 03  | **Flask-RESTX**                       | `Namespace` / `Resource`, Pydantic 스키마 등록, OpenAPI 문서                     | `controllers/console/**`, `controllers/common/schema.py`                 | -                 |
| 04  | **FastOpenAPI**                       | 타입 힌트 기반 라우팅(FastAPI 스타일) on Flask                                   | `controllers/fastopenapi.py`, `extensions/ext_fastopenapi.py`            | -                 |
| 05  | **SQLAlchemy 2.0 / Flask-SQLAlchemy** | `Mapped[]` 모델, naming convention, TypeDecorator, `select()` 쿼리, sessionmaker | `models/`, `core/db/session_factory.py`                                  | - (SQLite)        |
| 06  | **Flask-Migrate (Alembic)**           | init → autogenerate → upgrade → downgrade                                        | `migrations/`, `extensions/ext_migrate.py`                               | - (SQLite)        |
| 07  | **Flask-Login + PyJWT**               | `request_loader` 로 Bearer JWT 인증, 만료/변조 처리                              | `extensions/ext_login.py`, `libs/passport.py`                            | -                 |
| 08  | **Redis**                             | 캐시, 분산 락, Lua Rate Limit, Pub/Sub, Streams, Pipeline                        | `extensions/ext_redis.py`, `libs/helper.py`, `libs/broadcast_channel/`   | Redis             |
| 09  | **Celery**                            | FlaskTask(app_context), 큐 분리, `.delay()`, retry, beat 스케줄                  | `extensions/ext_celery.py`, `tasks/`, `schedule/`                        | Redis             |
| 10  | **gevent**                            | monkey patch, greenlet 동시성, Pool, CPU 바운드 주의점                           | `gunicorn.conf.py`, `celery_entrypoint.py`                               | -                 |
| 11  | **Gunicorn**                          | sync vs gevent vs GeventWebSocketWorker 처리량 비교                              | `docker/entrypoint.sh`, `gunicorn.conf.py`                               | -                 |
| 12  | **SSE 스트리밍 (httpx-sse)**          | `text/event-stream` 응답, `data:`/`event: ping` 포맷, 클라이언트 파싱            | `core/app/apps/base_app_generator.py`, `libs/helper.py`                  | -                 |
| 13  | **python-socketio**                   | 토큰 인증 connect, room, relay 브로드캐스트, RedisManager                        | `extensions/ext_socketio.py`, `controllers/console/socketio/workflow.py` | (선택) Redis      |
| 14  | **graphon (워크플로 엔진)**           | 커스텀 노드 + NodeFactory + GraphEngine 이벤트 스트림                            | `core/workflow/`, `graphon` 패키지                                       | -                 |
| 15  | **httpx**                             | 타임아웃, 재시도/백오프, 스트리밍, 이벤트 훅, **SSRF 프록시 차단**               | `core/helper/ssrf_proxy.py`                                              | (선택) ssrf_proxy |
| 16  | **OpenTelemetry**                     | TracerProvider, Flask/SQLAlchemy/httpx 자동 계측, 수동 span, X-Trace-Id          | `extensions/ext_otel.py`, `extensions/otel/`                             | -                 |

> Dify API 서버의 Swagger(OpenAPI) 문서 경로는 [SWAGGER.md](SWAGGER.md)를 참고하세요.

## 추천 학습 순서

1. **기반**: 01 → 02 → 03 → 04 (설정과 HTTP 레이어)
2. **데이터**: 05 → 06 (DB 모델과 스키마 마이그레이션)
3. **인증**: 07
4. **비동기/인프라**: 08 → 09 → 10 → 11 (Redis, 백그라운드 작업, 동시성 모델, 서버)
5. **실시간**: 12 → 13 (SSE 스트리밍, WebSocket 협업)
6. **Dify 핵심**: 14 (워크플로 엔진)
7. **운영**: 15 → 16 (외부 호출 보안, 관측성)

## 한 장으로 보는 요청 흐름

```
           ┌──────────── gunicorn (11) ── gevent worker (10) ─────────────┐
 browser ──┤  socketio.WSGIApp (13)                                       │
  / SDK    │    └─ Flask app  ← create_app() + ext_*.init_app() (02)      │
           │         ├─ Blueprint / Flask-RESTX / FastOpenAPI (03, 04)    │
           │         ├─ Flask-Login: JWT → Account (07)                   │
           │         ├─ Pydantic 검증 (01) → Service → SQLAlchemy (05,06) │
           │         ├─ Redis 캐시/락 (08)                                │
           │         ├─ 외부 호출 httpx → SSRF proxy (15)                 │
           │         └─ 응답: JSON 또는 SSE 스트림 (12)                   │
           └──────────────────────────────────────────────────────────────┘
                     │ .delay()                    ▲ 이벤트 (Redis Pub/Sub/Streams, 08)
                     ▼                             │
           ┌──── Celery worker (09) ───────────────┴────┐
           │  문서 인덱싱, 메일, 워크플로 실행 (14) ... │      OpenTelemetry (16): 전 구간 trace
           └────────────────────────────────────────────┘
```
