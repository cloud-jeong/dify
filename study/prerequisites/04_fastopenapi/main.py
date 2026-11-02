"""FastOpenAPI 예제 — Flask 위에서 FastAPI 스타일(타입 힌트 기반) 라우팅.

Dify 에서의 용도
  - Flask-RESTX 를 대체해 나가는 중인 신규 방식 (PoC).
      api/controllers/fastopenapi.py   : console_router = FlaskRouter()
      api/controllers/console/system.py: @console_router.get("/ping", response_model=PingResponse)
      api/controllers/console/setup.py : def setup_system(payload: SetupRequestPayload) -> SetupResponse
      api/extensions/ext_fastopenapi.py: 루트 FlaskRouter 에 include_router(prefix="/console/api")
  - 함수 시그니처의 Pydantic 타입으로 쿼리/바디를 자동 검증하고, OpenAPI 3.1 문서를 만들어 준다.
    (문서 위치: /fastopenapi/docs)

실행: uv run --project api python example/04_fastopenapi/main.py
"""

from fastopenapi.routers import FlaskRouter
from flask import Flask
from pydantic import BaseModel, Field

# 기능 모듈에서 쓰는 하위 라우터 (controllers/fastopenapi.py 의 console_router)
console_router = FlaskRouter()


class PingResponse(BaseModel):
    result: str


class VersionQuery(BaseModel):
    current_version: str = Field(..., description="client version")


class VersionResponse(BaseModel):
    version: str
    can_auto_update: bool


class SetupPayload(BaseModel):
    email: str = Field(..., pattern=r"^[^@]+@[^@]+$")
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class SetupResponse(BaseModel):
    result: str


@console_router.get("/ping", response_model=PingResponse, tags=["console"])
def ping() -> PingResponse:
    return PingResponse(result="pong")


@console_router.get("/version", response_model=VersionResponse, tags=["console"])
def check_version(query: VersionQuery) -> VersionResponse:  # ?current_version=... 가 query 로 들어온다
    return VersionResponse(version="1.17.1", can_auto_update=query.current_version < "1.17.1")


@console_router.post("/setup", response_model=SetupResponse, tags=["console"], status_code=201)
def setup(payload: SetupPayload) -> SetupResponse:  # JSON body 가 payload 로 검증되어 들어온다
    return SetupResponse(result=f"admin {payload.email} created")


def create_app() -> Flask:
    app = Flask(__name__)
    root = FlaskRouter(
        app=app,
        docs_url="/fastopenapi/docs",
        openapi_url="/fastopenapi/openapi.json",
        openapi_version="3.1.0",
        title="Demo API (FastOpenAPI)",
        version="1.0",
    )
    root.include_router(console_router, prefix="/console/api")
    return app


def main() -> None:
    c = create_app().test_client()
    print("GET  /ping     ->", c.get("/console/api/ping").get_json())
    print("GET  /version  ->", c.get("/console/api/version?current_version=1.10.0").get_json())
    r = c.get("/console/api/version")
    print("GET  /version (query 누락) ->", r.status_code, r.get_json())
    r = c.post("/console/api/setup", json={"email": "admin@example.com", "name": "admin", "password": "password123"})
    print("POST /setup    ->", r.status_code, r.get_json())
    r = c.post("/console/api/setup", json={"email": "nope", "name": "", "password": "x"})
    print("POST /setup (invalid) ->", r.status_code, r.get_json())

    spec = c.get("/fastopenapi/openapi.json").get_json()
    print("\nOpenAPI paths  :", list(spec["paths"].keys()))
    print("OpenAPI schemas:", list(spec.get("components", {}).get("schemas", {}).keys()))


if __name__ == "__main__":
    main()
