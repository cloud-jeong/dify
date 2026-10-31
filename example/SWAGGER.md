# Dify API 서버 Swagger(OpenAPI) 문서 경로

> 기준: Dify `1.17.1`, 로컬 API 서버 `http://localhost:5001`
> 검증: `uv run --project api flask routes`로 경로를 확인하고, 각 경로를 Flask test client로 요청해 200 응답을 확인함

Dify API 서버는 **API 그룹(Blueprint)마다 Swagger 문서가 따로** 있습니다.
경로 규칙은 모두 같습니다.

```
<prefix>/swagger-ui.html   ← Swagger UI (브라우저용 화면)
<prefix>/openapi.json      ← OpenAPI 3.1 스펙 (JSON)
```

---

## 1. 경로 목록

| API                   | 용도                                                | Swagger UI                                                                                                                 | OpenAPI JSON                | 엔드포인트 수 |
| --------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------- |
| **Console API**       | 관리 콘솔(웹 스튜디오)이 쓰는 API                   | [/console/api/swagger-ui.html](http://localhost:5001/console/api/swagger-ui.html)                                          | `/console/api/openapi.json` | 693           |
| **Service API**       | 외부 개발자용 공개 API (앱 API Key)                 | [/v1/swagger-ui.html](http://localhost:5001/v1/swagger-ui.html)                                                            | `/v1/openapi.json`          | 70            |
| **Web API**           | 공개된 WebApp(채팅 화면)용                          | [/api/swagger-ui.html](http://localhost:5001/api/swagger-ui.html)                                                          | `/api/openapi.json`         | 41            |
| **Files API**         | 파일 업로드·미리보기                                | [/files/swagger-ui.html](http://localhost:5001/files/swagger-ui.html)                                                      | `/files/openapi.json`       | 10            |
| **MCP API**           | MCP 서버로 노출된 앱                                | [/mcp/swagger-ui.html](http://localhost:5001/mcp/swagger-ui.html)                                                          | `/mcp/openapi.json`         | 1             |
| **Inner API**         | 내부 서비스 간 호출 (plugin daemon, enterprise)     | [/inner/api/swagger-ui.html](http://localhost:5001/inner/api/swagger-ui.html)                                              | `/inner/api/openapi.json`   | 39            |
| **FastOpenAPI** (PoC) | 신규 타입힌트 방식 라우트 (ping, version, setup 등) | [/fastopenapi/docs](http://localhost:5001/fastopenapi/docs), [/fastopenapi/redoc](http://localhost:5001/fastopenapi/redoc) | `/fastopenapi/openapi.json` | 4             |

- 엔드포인트 수는 `openapi.json`의 `paths` 개수이며, 버전에 따라 달라집니다.
- 모든 문서는 **로그인 없이 열람할 수 있습니다** (`SWAGGER_UI_ENABLED=true`일 때).

---

## 2. 관련 설정

`api/.env`에서 지정합니다.

```env
SWAGGER_UI_ENABLED=true            # false면 모든 Swagger UI와 openapi.json 비활성화
SWAGGER_UI_PATH=/swagger-ui.html   # 각 prefix 뒤에 붙는 UI 경로
```

| 항목                                                               | 위치                                                                             |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 설정 정의 (기본값 `True`, `/swagger-ui.html`)                      | `api/configs/feature/__init__.py`의 `SwaggerUIConfig`                            |
| 설정 적용 (`doc=SWAGGER_UI_PATH`, `add_specs=SWAGGER_UI_ENABLED`)  | `api/libs/external_api.py`의 `ExternalApi.__init__`                              |
| API별 prefix (`Blueprint(url_prefix=...)`)                         | `api/controllers/<console\|service_api\|web\|files\|mcp\|inner_api>/__init__.py` |
| FastOpenAPI 문서 경로 (하드코딩, `SWAGGER_UI_ENABLED`로만 켜고 끔) | `api/extensions/ext_fastopenapi.py`                                              |

설정을 바꾼 뒤에는 API 서버를 재시작해야 반영됩니다.

---

## 3. 주의할 점

### `/swagger.json`이 아니라 `/openapi.json`

Dify는 OpenAPI 3을 내보내는 **flask-restx 포크**를 씁니다 (`api/pyproject.toml`의 `[tool.uv.sources]` git 소스).
그래서 `/console/api/swagger.json`은 **404**가 나고, 스펙은 `/console/api/openapi.json`에 있습니다.

### 문서 열람은 무인증, API 호출(Try it out)은 인증 필요

Swagger UI 우측 상단의 **Authorize** 버튼에 토큰을 넣어야 "Try it out"으로 호출할 수 있습니다.

| API         | 넣을 값                                                    |
| ----------- | ---------------------------------------------------------- |
| Console API | 로그인 후 브라우저 쿠키의 `access_token` 값 (Bearer)       |
| Service API | 앱의 **API Key** (`app-xxxx`, 앱 → API 접근 메뉴에서 발급) |
| Web API     | WebApp passport 토큰                                       |

### 운영 환경

문서가 외부에 노출되지 않도록 `SWAGGER_UI_ENABLED=false`로 끄는 것이 좋습니다.

---

## 4. 활용 팁

```bash
# 전체 스펙을 파일로 받기 (Postman / Insomnia import, 클라이언트 코드 생성용)
curl -s http://localhost:5001/console/api/openapi.json -o console-openapi.json

# 특정 엔드포인트 찾기
curl -s http://localhost:5001/v1/openapi.json | jq '.paths | keys[]' | grep chat

# 서버를 띄우지 않고 등록된 문서 경로만 확인
uv run --project api flask routes | grep -Ei "swagger|openapi|/docs|redoc"
```

### 원하는 API의 컨트롤러 코드 찾기

1. 브라우저 DevTools → Network 탭에서 요청 경로를 확인합니다 (예: `/console/api/apps/<id>/workflows/draft/run`).
2. Swagger UI에서 같은 경로를 찾아 요청/응답 스키마를 확인합니다.
3. `api/controllers/`에서 경로 문자열(예: `"/apps/<uuid:app_id>/workflows/draft/run"`)로 검색하면 `@console_ns.route(...)`가 붙은 Resource 클래스가 나옵니다.
