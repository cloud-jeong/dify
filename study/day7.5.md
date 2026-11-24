1. Python 스레드와 GIL

- threading.Thread는 진짜 OS 스레드(pthread)를 만듭니다.
- 그런데 CPython에는 GIL(Global Interpreter Lock)이 있어서, 한 번에 한 스레드만 Python 바이트코드를 실행합니다.
  Dify가 쓰는 Python 3.13(api/pyproject.toml의 requires-python = "~=3.13.0")도 기본 빌드에는 GIL이 있습니다.
- 결과는 작업 종류에 따라 갈립니다.
  - CPU 바운드 작업(계산 위주): 스레드를 늘려도 빨라지지 않습니다. 이런 작업은 multiprocessing으로 풀어야 합니다.
  - I/O 바운드 작업(네트워크, DB, 파일): 스레드가 I/O를 기다리는 동안 GIL을 놓습니다. 그래서 다른 스레드가 실행될 수 있고, 동시성 효과가 충분히 납니다.

Dify의 \_generate_worker가 하는 일은 대부분 LLM API를 HTTP로 호출하고 응답을 기다리는 것입니다. 전형적인 I/O 바운드라서 GIL이 거의 문제가 되지 않습니다.

2. 여기서 스레드를 쓰는 이유: producer/consumer 구조

api/core/app/apps/chat/app_generator.py:231 주변은 이런 흐름입니다.

```auto
[요청 스레드]                                   [작업 스레드]
ChatAppGenerator.generate()
 ├ 입력 검증, 대화 조회, 설정 결정
 ├ _init_generate_records()  ← DB에 Conversation/Message 먼저 생성
 ├ QueueManager 생성 ───────────────────┐
 ├ Thread(_generate_worker).start() ───┼──▶ ChatAppRunner.run()
 │                                     │     ├ 모더레이션 / 어노테이션 / 지식 검색
 │                                     │     ├ invoke_llm(stream=True)
 │                                     │◀─── └ 청크마다 publish(QueueLLMChunkEvent) … 마지막 QueueMessageEndEvent
 └ _handle_response()                  │
    └ TaskPipeline._process_stream_response()
        for event in queue_manager.listen():  → SSE "message" … _save_message() → "message_end"
```

- worker 스레드(생산자)는 LLM 응답을 받아 queue_manager에 넣습니다.
- 요청 스레드(소비자)는 \_handle_response에서 큐를 읽어 바로 스트리밍합니다.
- 둘이 동시에 돌아야 토큰 단위 스트리밍이 됩니다. 병렬 계산을 하려는 게 아니라, 기다림을 겹치게 하려는 목적입니다.

부가적인 처리도 몇 가지 있습니다.

- @copy_current_request_context와 contextvars.copy_context(): 새 스레드에는 Flask의 request context와 contextvar가 없어서 복사해 넘깁니다.
- flask_app.app_context(): worker 안에서 app context를 새로 엽니다.
- finally: db.session.close(): 스레드별 DB 세션을 정리합니다.

3. 운영 환경에서는 스레드가 아니라 greenlet

- api/docker/entrypoint.sh:164의 gunicorn worker class 기본값은 geventwebsocket.gunicorn.workers.GeventWebSocketWorker입니다.
- api/app.py:12-14에는 monkey.patch_all()이 있고, api/gunicorn.conf.py는 psycopg와 grpc를 gevent에 맞게 패치합니다.

gevent의 monkey patching은 threading, socket, queue 같은 표준 라이브러리를 gevent 버전으로 바꿔치기합니다. 그래서 운영에서는 threading.Thread(...)가 OS 스레드가 아니라 greenlet(경량 코루틴)으로 만들어집니다.

- 하나의 OS 스레드 안에서 여러 greenlet이 돌아갑니다.
- 소켓 I/O를 만나면 다른 greenlet으로 협력적으로 전환됩니다.
- OS 스레드보다 훨씬 가벼워서, 동시 요청이 수천 개여도 감당할 수 있습니다.
- 대신 CPU를 오래 쓰는 코드가 있으면 그 프로세스의 다른 greenlet이 전부 멈춥니다.

정리

┌──────────────────────────┬─────────────────────────┬──────────────────────────────────┐
│ 환경 │ threading.Thread의 실체 │ 동시성 │
├──────────────────────────┼─────────────────────────┼──────────────────────────────────┤
│ gevent 없이 로컬 실행 │ OS 스레드 (GIL 있음) │ I/O 대기 중에만 다른 스레드 실행 │
├──────────────────────────┼─────────────────────────┼──────────────────────────────────┤
│ 운영 (gunicorn + gevent) │ greenlet │ I/O 지점에서 협력적으로 전환 │
└──────────────────────────┴─────────────────────────┴──────────────────────────────────┘

어느 쪽이든 이 코드는 LLM 응답을 기다리면서 동시에 스트리밍하는 게 목적이라, 두 환경 모두에서 의도대로 동작합니다. CPU를 많이 쓰는 작업(예: 문서 인덱싱)은 Celery 워커로 넘기는 구조입니다. CPU 병렬 처리는 프로세스를 나눠서 해결하는 셈입니다.

Cooked for 26s · done 8:54 PM

2026/11/24 12:55:40 /Users/cloudjung/git/dify-plugin-daemon/internal/db/executor.go:259 record not found
[0.607ms] [rows:0] SELECT * FROM "plugin_installations" WHERE tenant_id = 'e7cbf335-994e-43ab-b8ac-33366e85ddff' AND plugin_id = 'langgenius/azure_openai' ORDER BY "plugin_installations"."id" LIMIT 1

2026-11-24T12:55:40.076369Z INFO dify-plugin-daemon recycle.go:22 start new install task task_id=01a20da0-5129-72e6-9f3b-9255f4364685

2026-11-24T12:55:40.07637Z INFO dify-plugin-daemon middleware.go:83 trace_id=8c28b705397de529c5bbac0eaac874a2 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/identifiers status=200 latency_ms=4 client_ip=127.0.0.1 method=POST

2026-11-24T12:55:40.09008Z INFO dify-plugin-daemon middleware.go:83 trace_id=b35875342dee3522defe15cb49ee6713 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/tasks?page=1&page_size=100 status=200 latency_ms=0 client_ip=127.0.0.1

2026-11-24T12:55:40.090311Z INFO dify-plugin-daemon middleware.go:83 trace_id=1e5f215599b585293e3536f7a4f77644 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/tasks/01a20da0-5129-72e6-9f3b-9255f4364685 status=200 latency_ms=0 client_ip=127.0.0.1 method=GET

2026-11-24T12:55:40.099928Z INFO dify-plugin-daemon logger.go:15 local runtime starting plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1

2026-11-24T12:55:40.127584Z INFO dify-plugin-daemon launcher_local.go:78 acquiring distributed init lock plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1 expire=15m0s

2026-11-24T12:55:40.269209Z INFO dify-plugin-daemon setup_python_environment.go:450 detected dependency file plugin=langgenius/azure_openai:0.0.74 file=pyproject.toml

2026-11-24T12:55:40.269297Z INFO dify-plugin-daemon setup_python_environment.go:188 installing plugin dependencies plugin=langgenius/azure_openai:0.0.74 method="uv sync" file=pyproject.toml frozen=true

2026-11-24T12:55:40.269323Z INFO dify-plugin-daemon setup_python_environment.go:200 uv command cmd=/opt/homebrew/anaconda3/bin/uv args=[sync --no-dev --frozen -v]

2026-11-24T12:55:41.425025Z WARN dify-plugin-daemon setup_python_environment.go:244 failed to kill python process
error="os: process already finished"

2026-11-24T12:55:41.502976Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin file="Listing '.'..." more=true plugin=langgenius/azure_openai:0.0.74

2026-11-24T12:55:41.515411Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './.venv/lib/python3.12/site-packages/dotenv'..." more=true

2026-11-24T12:55:41.546732Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './.venv/lib/python3.12/site-packages/numpy/f2py/tests/src/regression'..." more=true

2026-11-24T12:55:41.555414Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './.venv/lib/python3.12/site-packages/openai/resources/audio'..." more=true

2026-11-24T12:55:41.562655Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './.venv/lib/python3.12/site-packages/pydantic-2.14.1.dist-info/licenses'..." more=true

2026-11-24T12:55:41.575484Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin more=true plugin=langgenius/azure_openai:0.0.74 file="Listing './cwd/.uv-cache/archive-v0/91kfyM9KHKOcyMpwm-Cbg/markupsafe-3.0.4.dist-info/licenses'..."

2026-11-24T12:55:41.584067Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './cwd/.uv-cache/archive-v0/FutQ8hOYljmfD0X3LejtN/openai/resources/admin/organization/users'..." more=true
2026-11-24T12:55:41.588996Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './cwd/.uv-cache/archive-v0/IIcjIi4QcFKeIwg5QTVKv/pydantic/experimental'..." more=true
2026-11-24T12:55:41.595171Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin plugin=langgenius/azure_openai:0.0.74 file="Listing './cwd/.uv-cache/archive-v0/ITG5laMrFCYo3eMBI_Wjj/numpy-2.5.4.dist-info/licenses/numpy'..." more=true
2026-11-24T12:55:41.64424Z INFO dify-plugin-daemon setup_python_environment.go:567 pre-compiling plugin more=true plugin=langgenius/azure_openai:0.0.74 file="Listing './cwd/.uv-cache/archive-v0/VTsKCgmsGh9UG7wPOF83K/msal_extensions-1.3.1.dist-info'..."

2026-11-24T12:55:41.650463Z INFO dify-plugin-daemon setup_python_environment.go:600 pre-loaded the plugin plugin=langgenius/azure_openai:0.0.74
2026-11-24T12:55:45.207269Z INFO dify-plugin-daemon middleware.go:83 trace_id=16b1161e76c647832b1ff578b65f7246 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/tasks?page=1&page_size=100 status=200 latency_ms=27 client_ip=127.0.0.1

2026-11-24T12:55:47.257746Z INFO dify-plugin-daemon launcher_local.go:115 released distributed init lock plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1

2026-11-24T12:55:47.257863Z INFO dify-plugin-daemon logger.go:76 local runtime scale up plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1 instance_nums=1

2026-11-24T12:55:49.619315Z INFO dify-plugin-daemon logger.go:61 plugin instance log plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1 instance=01a20da0 message="Installed model: azure_openai"

2026-11-24T12:55:49.620125Z INFO dify-plugin-daemon subprocess.go:184 local runtime instance ready instances_after=1 plugin=langgenius/azure_openai:0.0.74 instance=01a20da0 pid=53999 instances_before=0

2026-11-24T12:55:49.620174Z INFO dify-plugin-daemon logger.go:20 local runtime ready plugin=langgenius/azure_openai:0.0.74@5367feebcc35d7a17fa8e2cc53ae9d2382cb5ab6cc1001a239f10864f3d7dcf1

2026/11/24 12:55:49 /Users/cloudjung/git/dify-plugin-daemon/internal/db/executor.go:259 record not found
[2.913ms] [rows:0] SELECT * FROM "plugin_installations" WHERE plugin_id = 'langgenius/azure_openai' AND tenant_id = 'e7cbf335-994e-43ab-b8ac-33366e85ddff' ORDER BY "plugin_installations"."id" LIMIT 1

2026/11/24 12:55:49 /Users/cloudjung/git/dify-plugin-daemon/internal/db/executor.go:259 record not found
[0.445ms] [rows:0] SELECT * FROM "plugin_installations" WHERE plugin_id = 'langgenius/azure_openai' AND tenant_id = 'e7cbf335-994e-43ab-b8ac-33366e85ddff' ORDER BY "plugin_installations"."id" LIMIT 1
2026-11-24T12:55:49.650497Z INFO dify-plugin-daemon recycle.go:29 install task finished task_id=01a20da0-5129-72e6-9f3b-9255f4364685
2026-11-24T12:55:50.139106Z INFO dify-plugin-daemon middleware.go:83 trace_id=3aa57c4a2dfa1389c53ce9f4ddaba221 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request latency_ms=0 client_ip=127.0.0.1 method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/tasks/01a20da0-5129-72e6-9f3b-9255f4364685 status=200
2026-11-24T12:55:50.253867Z INFO dify-plugin-daemon middleware.go:83 trace_id=53749d7a24cd41f37243d686e2a52914 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/install/tasks?page=1&page_size=100 status=200 latency_ms=1 client_ip=127.0.0.1
2026-11-24T12:55:50.297925Z INFO dify-plugin-daemon middleware.go:83 trace_id=f0909790f0c3f92b689bfd6e5502ba0e tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/models/bindings status=200 latency_ms=8 client_ip=127.0.0.1
2026-11-24T12:55:50.30036Z INFO dify-plugin-daemon middleware.go:83 trace_id=b5784e2fde68309b093f82226ba5f6ee tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request status=200 latency_ms=9 client_ip=127.0.0.1 method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/installation/ids?category=model
2026-11-24T12:55:50.336215Z INFO dify-plugin-daemon middleware.go:83 trace_id=dc9b721cefefed02f424b923e37c1188 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request latency_ms=17 client_ip=127.0.0.1 method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/models?page=1&page_size=256 status=200
2026-11-24T12:55:50.851855Z INFO dify-plugin-daemon middleware.go:83 trace_id=f6f00f1aee63761bfdd24c03d54acfe1 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request method=POST path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/management/installation/fetch/batch status=200 latency_ms=12 client_ip=127.0.0.1
2026-11-24T12:55:51.020124Z INFO dify-plugin-daemon middleware.go:83 trace_id=0cdbe04ea824b5ab82e5c0388a6f6731 tenant_id=e7cbf335-994e-43ab-b8ac-33366e85ddff HTTP request client_ip=127.0.0.1 method=GET path=/plugin/e7cbf335-994e-43ab-b8ac-33366e85ddff/asset/d0672f274089e63184bfdf0167681843b5d3b5a84d21221e5216efc62034c80f.svg status=200 latency_ms=0
2026-11-24T12:56:15.577587Z INFO dify-plugin-daemon middleware.go:83 trace_id=5486458878f1b50dc460a380082b5890 HTTP request latency_ms=0 client_ip=172.30.1.31 method=GET path=/health/check status=200
2026-11-24T12:56:15.578867Z INFO dify-plugin-daemon middleware.go:83 trace_id=2b0c2778610264d08f1f56ec75497c2a HTTP request status=200 latency_ms=0 client_ip=192.168.139.2 method=GET path=/health/check
