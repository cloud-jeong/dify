# Dify 로컬 빌드 & 디버깅 가이드

> 저장소: https://github.com/langgenius/dify
> 기준 버전: 1.18.0 (`analysis` 브랜치)
> 작성일: 2026-11-01

이 문서는 **미들웨어(DB·Redis·벡터DB 등)는 Docker로, API·Worker·Web은 로컬 네이티브로** 실행하는 개발 방식을 기준으로 합니다. Python 패키지 관리는 `pip`/`venv`가 아니라 **`uv`**, 프론트엔드는 **`pnpm` 워크스페이스**를 사용하며, 반복 작업은 저장소 루트의 `dev/` 스크립트와 `Makefile`로 처리합니다.

---

## 1. 저장소 구조 개요

| 폴더                                 | 역할                                                                        |
| ------------------------------------ | --------------------------------------------------------------------------- |
| `api/`                               | 백엔드 API 서버 (Python 3.13, Flask + gevent, Celery)                       |
| `web/`                               | 프론트엔드 웹 UI (Next.js / React, `vp dev`로 개발 서버 실행)               |
| `packages/`                          | 프론트엔드 공용 패키지 (`dify-ui`, `contracts` 등, pnpm 워크스페이스)       |
| `docker/`                            | Docker Compose 배포 설정, `docker-compose.middleware.yaml`(개발용 미들웨어) |
| `dev/`                               | 로컬 개발용 셸 스크립트 (setup, start-\*, lint/type-check 등)               |
| `dify-agent/`, `dify-agent-runtime/` | 독립 에이전트 백엔드 및 샌드박스 런타임                                     |
| `cli/`, `sdks/`                      | CLI, 클라이언트 SDK                                                         |
| `e2e/`                               | Cucumber + Playwright E2E 테스트                                            |

---

## 2. 사전 준비 (필수 도구)

| 도구                             | 버전                                             | 비고                                                                      |
| -------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------- |
| Python                           | `~=3.13.0` (`api/pyproject.toml`)                | `uv`가 자동으로 설치/관리 가능                                            |
| [uv](https://docs.astral.sh/uv/) | 최신                                             | `brew install uv` 또는 `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js                          | `^24.22.1` (루트 `package.json` `engines`)       | nvm/fnm/volta 등으로 맞춤                                                 |
| pnpm                             | `12.10.1` (루트 `package.json` `packageManager`) | `corepack enable` 후 자동 사용 권장                                       |
| Docker / Docker Compose          | 최신                                             | 미들웨어 실행용                                                           |

```bash
git clone https://github.com/langgenius/dify.git
cd dify
corepack enable          # packageManager에 고정된 pnpm 버전 사용
uv python install 3.13   # (선택) uv로 Python 3.13 설치
```

> 이하 모든 명령은 **저장소 루트**에서 실행한다고 가정합니다. `dev/` 스크립트는 내부에서 스스로 경로를 잡기 때문에 어디서 실행해도 동작하지만, 루트 기준으로 통일하는 것이 편합니다.

---

## 3. 환경 초기 설정

두 가지 방법 중 하나를 사용합니다. **둘을 섞어 쓰지 않는 것**이 좋습니다(아래 3.3 주의 참고).

### 3.1 방법 A — `dev/` 스크립트 (공식 권장)

```bash
./dev/setup
```

`dev/setup`이 하는 일:

1. `api/.env.example` → `api/.env`
2. `web/.env.example` → `web/.env.local`
3. `docker/envs/middleware.env.example` → `docker/middleware.env`
4. `cd api && uv sync --group dev` (Python 의존성 + dev 그룹 설치, `api/.venv` 생성)
5. `pnpm --dir <root> install` (루트 워크스페이스 기준 JS 의존성 설치)

> ⚠️ `dev/setup`은 env 파일을 **무조건 덮어씁니다**(`cp`). 이미 수정한 `api/.env`, `web/.env.local`, `docker/middleware.env`가 있다면 백업 후 실행하세요.

### 3.2 방법 B — `Makefile` 타깃

```bash
make dev-setup     # = prepare-docker + prepare-web + prepare-api
```

| 타깃                  | 동작                                                                                                  |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| `make prepare-docker` | `docker/middleware.env`가 없을 때만 생성 → 미들웨어 컨테이너 기동 (프로젝트명 `dify-middlewares-dev`) |
| `make prepare-web`    | `web/.env.local`이 없을 때만 생성(`cp -n`) → `pnpm install`                                           |
| `make prepare-api`    | `api/.env`가 없을 때만 생성 → `uv sync --dev` → `uv run flask db upgrade`                             |
| `make dev-clean`      | 미들웨어 down + `docker/volumes/*`, `api/storage` 삭제 (**데이터 초기화**)                            |

Makefile 방식은 기존 env 파일을 **덮어쓰지 않으며**, DB 마이그레이션까지 한 번에 수행합니다.

### 3.3 주의: Compose 프로젝트명 차이

| 실행 방법                                | Compose 프로젝트명(`-p`) |
| ---------------------------------------- | ------------------------ |
| `./dev/start-docker-compose`             | `dify`                   |
| `make prepare-docker` / `make dev-clean` | `dify-middlewares-dev`   |

두 방법을 섞으면 같은 포트(5432, 6379 등)를 쓰는 컨테이너가 **두 세트** 생겨 포트 충돌이 나거나, `make dev-clean`이 `dev/start-docker-compose`로 띄운 컨테이너를 내리지 못합니다. 한 가지로 통일하고, 필요하면 수동으로 정리합니다.

```bash
cd docker
docker compose -f docker-compose.middleware.yaml --env-file middleware.env -p dify down
```

### 3.4 env 파일 검토 포인트

- **`api/.env`**
  - `SECRET_KEY`: 비워두면 storage 디렉토리에 영구 키를 자동 생성. 직접 관리하려면 `openssl rand -base64 42`로 생성해 설정
  - DB/Redis/벡터DB 접속 정보가 `docker/middleware.env`의 포트와 일치하는지 확인
- **`web/.env.local`**
  - `NEXT_PUBLIC_API_PREFIX=http://localhost:5001/console/api`
  - `NEXT_PUBLIC_PUBLIC_API_PREFIX=http://localhost:5001/api`
  - 프론트와 백엔드를 서로 다른 서브도메인에 둘 경우 `COOKIE_DOMAIN`(api) / `NEXT_PUBLIC_COOKIE_DOMAIN`(web)을 최상위 도메인으로 맞춰야 인증 쿠키가 공유됨
- **`docker/middleware.env`**
  - `COMPOSE_PROFILES=${DB_TYPE:-postgresql},weaviate` — 기본은 PostgreSQL + Weaviate. MySQL을 쓰려면 `DB_TYPE=mysql`
  - 노출 포트: `EXPOSE_*_PORT` 변수로 변경 가능

---

## 4. 서비스 실행

각 장기 실행 프로세스는 **터미널을 따로** 띄워 실행합니다.

### 4.1 미들웨어 (Docker)

```bash
./dev/start-docker-compose
# 내부: cd docker && docker compose --env-file middleware.env -f docker-compose.middleware.yaml -p dify up -d

# 실행확인
docker compose -p dify ps
docker compose -p dify logs -f plugin_daemon

# down & cleansing
make dev-clean
# 내부 cd docker & docker compose -f docker-compose.middleware.yaml --env-file middleware.env -p dify down
#  rm -rf docker/volumes/db docker/volumes/mysql docker/volumes/redis docker/volumes/plugin_daemon docker/volumes/weaviate docker/volumes/sandbox/dependencies
#	 rm -rf api/storage
```

기본 기동 서비스와 포트:

| 서비스          | 포트               | 용도                       |
| --------------- | ------------------ | -------------------------- |
| `db_postgres`   | 5432               | 메타데이터 DB              |
| `redis`         | 6379               | 캐시, Celery 브로커        |
| `weaviate`      | 8080 / 50051(gRPC) | 벡터 DB (RAG)              |
| `sandbox`       | 8194               | 코드 실행 샌드박스         |
| `plugin_daemon` | 5002 (디버깅 5003) | 플러그인 런타임            |
| `ssrf_proxy`    | 3128               | 외부 요청 SSRF 방지 프록시 |
| `local_sandbox` | 5004               | dify-agent 로컬 샌드박스   |

### 4.2 API 서버

```bash
./dev/start-api
```

내부 동작:

```bash
cd api
uv run flask db upgrade                                    # 마이그레이션 자동 적용
uv run dotenv -f .env run --no-override -- python -m app   # gevent pywsgi 서버로 :5001 기동
```

- `python -m app`은 `app.py` 하단의 **gevent pywsgi + WebSocket 핸들러**로 서빙합니다. 실행 전에 `gevent.monkey.patch_all()`과 psycopg/grpc gevent 패치를 적용하므로, 운영(gunicorn gevent worker)과 동작이 가장 가깝습니다.
- `flask run`도 동작은 하지만 Werkzeug 스레드 모델이고 WebSocket(`NEXT_PUBLIC_SOCKET_URL`)을 처리하지 않으므로, 로컬 개발에는 `dev/start-api`(= `python -m app`)를 권장합니다.
- `--no-override`: 셸에 이미 export된 환경변수가 `.env` 값보다 우선합니다. 일회성으로 설정을 바꿔 띄울 때 유용합니다.
  ```bash
  LOG_LEVEL=DEBUG ./dev/start-api
  ```

### 4.3 Web (프론트엔드)

```bash
./dev/start-web
# 내부: pnpm --dir <root> install && pnpm --dir web dev   (vp dev)
```

- 브라우저에서 `http://localhost:3000` 접속 → 최초 접속 시 관리자 계정 설정(`/install`)
- 별도로 `cd web && pnpm install` 할 필요 없음 (루트 워크스페이스에서 설치)
- 기타 web 스크립트 (`pnpm --dir web <script>`)

| 스크립트                     | 용도                                                                  |
| ---------------------------- | --------------------------------------------------------------------- |
| `dev`                        | 기본 개발 서버 (`vp dev`)                                             |
| `dev:next`                   | Next.js 개발 서버 (`next dev`)                                        |
| `dev:next:inspect`           | `next dev --inspect` — Node 디버거 attach 가능                        |
| `dev:proxy`                  | 로컬 API 없이 원격(`DEV_PROXY_TARGET`, 기본 cloud.dify.ai)으로 프록시 |
| `build` / `start`            | 프로덕션 빌드 / 실행                                                  |
| `type-check`, `test`, `lint` | 타입 체크 / Vitest / Lint                                             |

> 참고: 이 브랜치에서는 `web/app/components/devtools/react-scan/loader.tsx`에서 React Scan을 로컬에서 비활성화해 두었습니다(커밋 `4fe0fa6a42`). 렌더링 성능 분석이 필요하면 `|| true`를 제거하세요.

### 4.4 Celery Worker (비동기 작업)

문서 인덱싱, 워크플로우 비동기 실행, 메일 발송, 플러그인 작업 등은 Worker가 있어야 처리됩니다. **지식베이스(RAG) 문서 업로드를 테스트하려면 반드시 실행**해야 합니다.

```bash
./dev/start-worker                                   # 에디션별 기본 큐 전체, gevent, concurrency 1
./dev/start-worker --queues dataset,workflow         # 특정 큐만 처리
./dev/start-worker -q dataset -c 2 -P prefork        # 풀/동시성 변경
./dev/start-worker --loglevel DEBUG -e ./my.env      # 로그 레벨, 추가 env 파일 로드
./dev/start-worker --help                            # 큐 목록 및 옵션
```

주요 큐: `dataset`(RAG 인덱싱), `workflow`(워크플로우), `mail`, `plugin`, `ops_trace`, `schedule_poller`/`schedule_executor`(스케줄 트리거) 등. `DEPLOYMENT_EDITION=CLOUD`이면 `workflow_professional/team/sandbox` 큐가 대신 사용됩니다.

### 4.5 Celery Beat (주기 작업, 선택)

```bash
./dev/start-beat
./dev/start-beat --loglevel DEBUG
```

스케줄 트리거, 정리(retention) 작업 등 주기 작업이 필요할 때 실행합니다. `KNOWLEDGE_FS_LIFECYCLE_WORKER_ENABLED=true`인 경우 필수입니다.

### 4.6 실행 순서 요약

```bash
# 최초 1회
./dev/setup
#   → api/.env, web/.env.local, docker/middleware.env 검토

# 매번 (각각 별도 터미널)
./dev/start-docker-compose   # 1. 미들웨어
./dev/start-api              # 2. API      :5001 (마이그레이션 포함)
./dev/start-worker           # 3. Worker
./dev/start-web              # 4. Web      :3000
./dev/start-beat             # 5. (선택) Beat
```

---

## 5. uv 활용 팁

AGENTS.md 규칙에 따라 백엔드 명령은 **`uv run --project api <command>`** 형태로 실행합니다(가상환경 activate 불필요).

| 작업                   | 명령                                                                                    |
| ---------------------- | --------------------------------------------------------------------------------------- |
| 의존성 동기화          | `uv sync --project api --group dev`                                                     |
| 패키지 추가            | `uv add --project api <pkg>` / dev: `uv add --project api --group dev <pkg>`            |
| lock 파일 검증         | `./dev/sync-uv` (`uv lock --project api`)                                               |
| 의존성 전체 업그레이드 | `./dev/update-uv` (`uv lock --project api --upgrade` 후 `--check`)                      |
| Flask CLI              | `uv run --project api flask --app api/app.py <cmd>` 또는 `cd api && uv run flask <cmd>` |
| DB 마이그레이션 적용   | `cd api && uv run flask db upgrade`                                                     |
| 마이그레이션 생성      | `cd api && uv run flask db revision --autogenerate -m "<msg>"`                          |
| Python REPL            | `cd api && uv run flask shell` (앱 컨텍스트 포함)                                       |
| 임의 스크립트          | `uv run --project api python <script.py>`                                               |

> `uv run --project api`는 `api/pyproject.toml`과 `api/.venv`를 사용하지만 **작업 디렉토리는 바뀌지 않습니다**. `api/.env`를 읽어야 하는 Flask 명령은 `cd api` 후 실행하거나 `uv run --directory api ...`를 사용하세요.

---

## 6. 코드 품질 / 테스트

| 작업                 | Makefile                                                         | dev 스크립트 / 직접 실행                                                  |
| -------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 포맷                 | `make format`                                                    | `uv run --project api --dev ruff format ./api`                            |
| 린트 체크            | `make check`                                                     | `uv run --project api --dev ruff check ./api`                             |
| 전체 린트(+자동수정) | `make lint`                                                      | `./dev/reformat` (import-linter, ruff fix/format, dotenv-linter, pyrefly) |
| 타입 체크            | `make type-check` / `make type-check PATH_TO_CHECK=api/services` | `./dev/pyrefly-check-local [path...]`, `./dev/ty-check`                   |
| 단위 테스트          | `make test`                                                      | —                                                                         |
| 특정 테스트          | `make test TARGET_TESTS=./api/tests/unit_tests/<path>`           | `uv run --project api --dev pytest <path> -k <name>`                      |
| 응답 계약 린트       | `make api-contract-lint`                                         | —                                                                         |

- 통합 테스트(`make test-all`)는 Docker 기반이며 **CI 전용**입니다. 로컬에서는 단위 테스트까지만 실행합니다.
- 프론트엔드: `pnpm --dir web test`, `pnpm --dir web type-check`, `pnpm --dir web lint`
- API 계약(OpenAPI/Zod) 재생성: `pnpm -C packages/contracts gen-api-contract`

---

## 7. 로컬 디버깅

### 7.1 VS Code / Cursor — 루트 워크스페이스 기준 (권장)

```bash
cp .vscode/launch.json.template .vscode/launch.json
```

제공 구성:

| 이름                           | 내용                                                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `Python: API (gevent)`         | `python -m gevent.monkey --module app`, `gevent: true`, cwd=`api/`, 인터프리터 `api/.venv/bin/python`  |
| `Python: Celery Worker (Solo)` | `celery -A app.celery worker -P solo -c 1 -Q <전체 큐>` — solo 풀이라 브레이크포인트가 안정적으로 걸림 |

절차:

1. `./dev/setup`(또는 `uv sync --project api --group dev`)으로 `api/.venv` 생성
2. 미들웨어만 기동: `./dev/start-docker-compose`
3. 마이그레이션: `cd api && uv run flask db upgrade` (`dev/start-api`를 쓰지 않으므로 직접 실행)
4. Run and Debug(⇧⌘D)에서 `Python: API (gevent)` 선택 → F5
5. Worker 코드를 디버깅하려면 `./dev/start-worker` 대신 `Python: Celery Worker (Solo)`로 실행
6. Web은 터미널에서 `./dev/start-web`

> **주의**: 디버거로 API를 띄울 때는 `./dev/start-api`를 동시에 실행하지 마세요(포트 5001 충돌). Worker도 마찬가지로 디버거/스크립트 중 하나만 실행합니다.

### 7.2 VS Code — `api/` 폴더를 워크스페이스로 여는 경우

`api/.vscode/launch.json.example`을 `api/.vscode/launch.json`으로 복사합니다. `envFile: .env`를 사용하며, `Launch Flask and Celery` compound로 API + Worker를 동시에 디버깅할 수 있습니다.

### 7.3 PyCharm

- Interpreter: `api/.venv/bin/python` (uv가 만든 venv를 Existing environment로 지정)
- Run configuration: Module `app`, Working directory `api/`, EnvFile `api/.env`
- Settings → Python Debugger → **Gevent compatible** 체크 (gevent 기반이므로 필수)

### 7.4 원격/컨테이너 attach (debugpy)

```bash
cd api
# debugpy는 프로젝트 의존성에 없으므로 --with로 임시 주입
uv run --with debugpy python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m gevent.monkey --module app
```

IDE에서 `"request": "attach"`, `"connect": {"host": "localhost", "port": 5678}`, `"gevent": true`로 연결합니다.

### 7.5 프론트엔드 디버깅

- 브라우저 DevTools (Network 탭에서 `/console/api/*` 요청 확인)
- Node 측(SSR/Route handler) 디버깅: `pnpm --dir web dev:next:inspect` 후 `chrome://inspect` 또는 VS Code "Attach to Node Process"
- 백엔드 없이 UI만 개발: `pnpm --dir web dev:proxy` (원격 API로 프록시)

### 7.6 핫 리로드

- Web: `vp dev`/`next dev`가 변경 즉시 반영
- API: `python -m app`(gevent)은 자동 리로드가 없으므로 Python 코드 수정 후 **재시작** 필요 (디버거에서는 Restart ⇧⌘F5)
- Worker: 마찬가지로 재시작 필요

### 7.7 자주 겪는 문제

| 증상                                     | 원인 / 해결                                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 포트 5432/6379 이미 사용 중              | 로컬 Postgres/Redis 또는 다른 Compose 프로젝트(`dify` vs `dify-middlewares-dev`)가 실행 중 → 정리하거나 `EXPOSE_*_PORT` 변경 |
| 문서 업로드 후 "인덱싱 대기" 상태로 멈춤 | Worker 미실행 또는 `dataset` 큐 누락 → `./dev/start-worker`                                                                  |
| 플러그인/모델 프로바이더 설치 실패       | `plugin_daemon` 컨테이너 로그 확인, `api/.env`의 `PLUGIN_DAEMON_URL`·키가 `middleware.env`와 일치하는지 확인                 |
| 디버거에서 요청 처리 중 프로세스가 멈춤  | gevent 패치 없이 실행됨 → `gevent.monkey` 모듈 경유 실행 + IDE gevent 지원 옵션 활성화                                       |
| `uv sync` 후에도 모듈을 못 찾음          | `api/.venv`가 아닌 다른 인터프리터 사용 중 → IDE 인터프리터 경로 확인                                                        |
| 마이그레이션 오류 / DB 꼬임              | `make dev-clean`으로 볼륨 초기화 후 재기동 (**데이터 삭제됨**)                                                               |

---

## 8. 전체 아키텍처 개요

```
Browser ──▶ Web (Next.js :3000)
               │  /console/api, /api, ws
               ▼
           API (Flask + gevent :5001) ──▶ PostgreSQL :5432
               │        │                Redis :6379 (캐시/브로커)
               │        │                Weaviate :8080 (벡터)
               │        ├──▶ Plugin Daemon :5002 ──▶ 모델/툴 플러그인
               │        └──▶ Sandbox :8194 (코드 노드) ──▶ SSRF Proxy :3128
               ▼
           Redis 큐 ──▶ Celery Worker (인덱싱, 워크플로우, 메일 …)
                        Celery Beat (주기 작업 스케줄링)
```

- **API 서버 (`api/`)**: 인증, 앱/워크플로우 관리, LLM 호출 오케스트레이션, RAG 파이프라인. 개발 시 `python -m app`(gevent pywsgi), 운영 시 gunicorn gevent worker
- **Celery Worker / Beat**: 문서 인덱싱·요약, 비동기 워크플로우, 스케줄 트리거, 정리 작업
- **웹 UI (`web/`)**: 워크플로우 빌더, 앱 관리 대시보드, 챗 인터페이스
- **Plugin Daemon**: 모델 프로바이더·툴·에이전트 전략을 플러그인으로 실행 (LLM 통합 계층)
- **Sandbox / SSRF Proxy**: 코드 노드 격리 실행, 외부 HTTP 요청 통제

---

## 9. 참고 문서

- `api/README.md` — 백엔드 셋업 공식 가이드 (dev 스크립트 기준)
- `web/README.md` — 프론트엔드 가이드
- `.vscode/README.md` — VS Code 디버깅 구성
- `api/AGENTS.md`, `web/AGENTS.md` — 영역별 코드 컨벤션
- `docker/docker-compose.middleware.yaml`, `docker/envs/middleware.env.example` — 미들웨어 구성
- 전체 스택을 컨테이너로만 띄우려면 `docker/docker-compose.yaml` 사용 (디버깅 목적이라면 미들웨어만 컨테이너로 띄우는 방식이 유리)

---

## 주1. mac에서 설치된 python version 리스트업 및 default 설정

```
uv python list
uv python install 3.13 --default
which -a python3 python
```

/usr/bin/python3(macOS 기본 3.9)는 시스템이 관리하는 파일이니 지우거나 덮어쓰지 안됨. PATH 우선순위만으로 바꾸는 게 안전함.
