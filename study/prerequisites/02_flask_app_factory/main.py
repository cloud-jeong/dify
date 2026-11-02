"""Flask App Factory + Extension 패턴 예제.

Dify 에서의 용도
  - api/app.py → app_factory.create_app()
  - api/app_factory.py 의 initialize_extensions():
      extensions/ext_*.py 모듈마다 `init_app(app)` (선택적으로 `is_enabled()`) 가 있고,
      순서가 의미 있는 리스트를 돌며 하나씩 초기화한다. (DB → Redis → Storage → Celery → Login → Blueprints ...)
  - api/dify_app.py: Flask 를 상속한 DifyApp
  - api/extensions/ext_blueprints.py: console / service_api / web / files 등 Blueprint 등록 + CORS

실행: uv run --project api python example/02_flask_app_factory/main.py
"""

import logging
import time
import types

from flask import Blueprint, Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("factory")


class DemoApp(Flask):
    """DifyApp 처럼 Flask 를 상속해 확장 속성 타입을 붙여둘 수 있다."""


# ---------------------------------------------------------------------------
# Extension 모듈 흉내: 실제로는 extensions/ext_xxx.py 파일 하나하나가 모듈이다.
# ---------------------------------------------------------------------------
def _make_ext(name: str, init_app, is_enabled=None) -> types.ModuleType:
    mod = types.ModuleType(f"extensions.{name}")
    mod.init_app = init_app
    if is_enabled:
        mod.is_enabled = is_enabled
    return mod


def _init_config(app: DemoApp) -> None:
    app.config["APP_VERSION"] = "1.0.0-demo"


def _init_fake_db(app: DemoApp) -> None:
    app.extensions["db"] = {"apps": [{"id": "1", "name": "Hello Bot"}]}


def _init_blueprints(app: DemoApp) -> None:
    # Dify: console(/console/api), service_api(/v1), web(/api), files(/files), inner_api ...
    console_bp = Blueprint("console", __name__, url_prefix="/console/api")
    service_bp = Blueprint("service_api", __name__, url_prefix="/v1")

    @console_bp.get("/apps")
    def list_apps():
        return jsonify(data=app.extensions["db"]["apps"])

    @service_bp.get("/info")
    def info():
        return jsonify(version=app.config["APP_VERSION"])

    @console_bp.get("/boom")
    def boom():
        raise RuntimeError("unexpected")

    CORS(console_bp, supports_credentials=True)  # 블루프린트별로 CORS 정책을 다르게
    CORS(service_bp, origins="*")
    app.register_blueprint(console_bp)
    app.register_blueprint(service_bp)


EXTENSIONS = [
    _make_ext("ext_config", _init_config),
    _make_ext("ext_database", _init_fake_db),
    _make_ext("ext_sentry", lambda app: None, is_enabled=lambda: False),  # 설정에 따라 꺼지는 확장
    _make_ext("ext_blueprints", _init_blueprints),
]


def initialize_extensions(app: DemoApp) -> None:
    for ext in EXTENSIONS:
        short = ext.__name__.split(".")[-1]
        if hasattr(ext, "is_enabled") and not ext.is_enabled():
            logger.info("Skipped %s", short)
            continue
        start = time.perf_counter()
        ext.init_app(app)
        logger.info("Loaded %s (%.2f ms)", short, (time.perf_counter() - start) * 1000)


def create_app() -> DemoApp:
    app = DemoApp(__name__)

    # app_factory.create_flask_app_with_configs() 처럼 요청 훅을 건다
    @app.before_request
    def before_request():
        g.start = time.perf_counter()

    @app.after_request
    def after_request(resp):
        resp.headers["X-Elapsed-ms"] = f"{(time.perf_counter() - g.start) * 1000:.2f}"
        return resp

    # libs/external_api.py 의 ExternalApi 처럼 에러를 JSON 으로 통일
    @app.errorhandler(Exception)
    def handle_error(e: Exception):
        if isinstance(e, HTTPException):
            return jsonify(code=e.name, message=e.description, status=e.code), e.code
        logger.exception("Unhandled error on %s", request.path)
        return jsonify(code="internal_server_error", message=str(e), status=500), 500

    initialize_extensions(app)
    return app


def main() -> None:
    app = create_app()
    print("\n등록된 라우트:")
    for rule in app.url_map.iter_rules():
        print("  ", rule.rule, sorted(rule.methods - {"HEAD", "OPTIONS"}))

    client = app.test_client()  # 실제 서버 없이 요청을 보내볼 수 있다 (Dify 단위 테스트도 이 방식)
    for path in ["/console/api/apps", "/v1/info", "/nope", "/console/api/boom"]:
        r = client.get(path)
        print(f"\nGET {path} -> {r.status_code} {r.get_json()} elapsed={r.headers.get('X-Elapsed-ms')}ms")


if __name__ == "__main__":
    main()
