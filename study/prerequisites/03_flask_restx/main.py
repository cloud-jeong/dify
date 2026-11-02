"""Flask-RESTX (Api / Namespace / Resource) + Pydantic 스키마 예제.

Dify 에서의 용도
  - 대부분의 HTTP API 는 Flask-RESTX 의 클래스 기반 Resource 로 작성되어 있다.
      api/controllers/console/__init__.py  : Blueprint("console") + ExternalApi + console_ns(Namespace)
      api/controllers/console/app/app.py   : @console_ns.route("/apps") class AppListApi(Resource)
  - 요청/응답 스키마는 Pydantic 으로 정의하고 controllers/common/schema.py 의
    register_schema_models() 로 Namespace 에 JSON Schema 를 등록 → Swagger 문서(/console/api/docs) 생성
  - 핸들러 안에서는 `Payload.model_validate(console_ns.payload)` 로 검증한다.

실행: uv run --project api python example/03_flask_restx/main.py
"""

import json
import uuid
from http import HTTPStatus

from flask import Blueprint, Flask, request
from flask_restx import Api, Namespace, Resource
from pydantic import BaseModel, Field, ValidationError
from werkzeug.exceptions import BadRequest, NotFound

# ---------------------------------------------------------------------------
# Blueprint + Api + Namespace  (controllers/console/__init__.py 구조)
# ---------------------------------------------------------------------------
bp = Blueprint("console", __name__, url_prefix="/console/api")
api = Api(bp, version="1.0", title="Demo Console API", doc="/docs")
console_ns = Namespace("console", description="Console management APIs", path="/")
api.add_namespace(console_ns)


# ---------------------------------------------------------------------------
# Pydantic 스키마 → Namespace 에 등록 (controllers/common/schema.py 단순화 버전)
# ---------------------------------------------------------------------------
class CreateAppPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=40)
    mode: str = Field(default="chat", pattern="^(chat|workflow|agent-chat)$")


class AppItem(BaseModel):
    id: str
    name: str
    mode: str


class AppPagination(BaseModel):
    page: int
    limit: int
    total: int
    data: list[AppItem]


def register_schema_models(ns: Namespace, *models: type[BaseModel]) -> None:
    for model in models:
        schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        for name, sub in schema.pop("$defs", {}).items():
            ns.schema_model(name, sub)
        ns.schema_model(model.__name__, schema)


register_schema_models(console_ns, CreateAppPayload, AppItem, AppPagination)

_APPS: dict[str, AppItem] = {}


# ---------------------------------------------------------------------------
# Resource 클래스: 메서드 이름(get/post/delete)이 곧 HTTP 메서드
# ---------------------------------------------------------------------------
@console_ns.route("/apps")
class AppListApi(Resource):
    @console_ns.doc("list_apps", params={"page": "page number", "limit": "page size"})
    @console_ns.response(HTTPStatus.OK, "Success", console_ns.models["AppPagination"])
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)
        items = list(_APPS.values())
        sliced = items[(page - 1) * limit : page * limit]
        return AppPagination(page=page, limit=limit, total=len(items), data=sliced).model_dump()

    @console_ns.doc("create_app")
    @console_ns.expect(console_ns.models["CreateAppPayload"])
    @console_ns.response(HTTPStatus.CREATED, "Created", console_ns.models["AppItem"])
    def post(self):
        try:
            payload = CreateAppPayload.model_validate(console_ns.payload or {})
        except ValidationError as e:
            raise BadRequest(e.errors()[0]["msg"])
        app = AppItem(id=str(uuid.uuid4()), name=payload.name, mode=payload.mode)
        _APPS[app.id] = app
        return app.model_dump(), HTTPStatus.CREATED


@console_ns.route("/apps/<uuid:app_id>")
class AppApi(Resource):
    def get(self, app_id: uuid.UUID):
        app = _APPS.get(str(app_id))
        if not app:
            raise NotFound("App not found")  # restx 가 {"message": ...} JSON 으로 변환
        return app.model_dump()

    def delete(self, app_id: uuid.UUID):
        _APPS.pop(str(app_id), None)
        return {"result": "success"}, HTTPStatus.NO_CONTENT


def main() -> None:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(bp)
    c = flask_app.test_client()

    r = c.post("/console/api/apps", json={"name": "Support Bot", "mode": "chat"})
    print("POST /apps          ->", r.status_code, r.get_json())
    app_id = r.get_json()["id"]

    r = c.post("/console/api/apps", json={"name": "", "mode": "bad"})
    print("POST /apps (invalid) ->", r.status_code, r.get_json())

    print("GET  /apps          ->", c.get("/console/api/apps?page=1&limit=10").get_json())
    print("GET  /apps/<id>     ->", c.get(f"/console/api/apps/{app_id}").status_code)
    print("GET  /apps/<random> ->", c.get(f"/console/api/apps/{uuid.uuid4()}").get_json())

    # Dify 가 쓰는 flask-restx 포크(pyproject.toml 의 git 소스)는 OpenAPI 3 문서를 /openapi.json 으로 낸다
    spec = c.get("/console/api/openapi.json").get_json()
    print("\nOpenAPI version :", spec.get("openapi"))
    print("OpenAPI paths   :", list(spec["paths"].keys()))
    print("OpenAPI schemas :", list(spec["components"]["schemas"].keys()))
    print("POST /apps body :", json.dumps(spec["paths"]["/apps"]["post"].get("requestBody")))
    print("\n(브라우저로 보려면 flask_app.run() 후 http://127.0.0.1:5000/console/api/docs)")


if __name__ == "__main__":
    main()
