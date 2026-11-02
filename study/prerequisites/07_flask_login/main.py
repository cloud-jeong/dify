"""Flask-Login + JWT(PyJWT) 토큰 인증 예제.

Dify 에서의 용도
  - api/extensions/ext_login.py
      * DifyLoginManager(flask_login.LoginManager)
      * @login_manager.request_loader: 쿠키 세션이 아니라 "요청마다" 토큰을 읽어 사용자를 로드
          - console blueprint  → Authorization: Bearer <JWT> (또는 access_token 쿠키) → Account
          - web blueprint      → WebApp passport 토큰 → EndUser
      * @login_manager.unauthorized_handler: 항상 JSON 401 응답
  - api/libs/passport.py : PassportService — SECRET_KEY 로 HS256 JWT 발급/검증
  - api/libs/login.py    : @login_required, current_user, current_account_with_tenant()

실행: uv run --project api python example/07_flask_login/main.py
"""

import json
from datetime import UTC, datetime, timedelta

import jwt
from flask import Blueprint, Flask, Response, jsonify, request
from flask_login import LoginManager, UserMixin, current_user, login_required
from werkzeug.exceptions import Unauthorized

SECRET_KEY = "demo-secret-key-at-least-32-bytes-long!"  # Dify: dify_config.SECRET_KEY


# ---------------------------------------------------------------------------
# PassportService (libs/passport.py)
# ---------------------------------------------------------------------------
class PassportService:
    def issue(self, payload: dict) -> str:
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def verify(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired.")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token.")


# ---------------------------------------------------------------------------
# 사용자 모델 (models/account.py 의 Account 단순화)
# ---------------------------------------------------------------------------
class Account(UserMixin):
    def __init__(self, id: str, email: str, password: str, current_tenant_id: str):
        self.id = id
        self.email = email
        self.password = password
        self.current_tenant_id = current_tenant_id


ACCOUNTS = {"u1": Account("u1", "admin@example.com", "password123", current_tenant_id="t1")}


# ---------------------------------------------------------------------------
# LoginManager — request_loader 방식 (ext_login.py)
# ---------------------------------------------------------------------------
login_manager = LoginManager()


def extract_access_token(req) -> str | None:  # libs/token.py
    auth = req.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:]
    return req.cookies.get("access_token")


@login_manager.request_loader
def load_user_from_request(req) -> Account | None:
    if request.blueprint == "console":
        token = extract_access_token(req)
        if not token:
            raise Unauthorized("Invalid Authorization token.")
        decoded = PassportService().verify(token)
        return ACCOUNTS.get(decoded.get("user_id", ""))
    return None


@login_manager.unauthorized_handler
def unauthorized_handler() -> Response:
    return Response(
        json.dumps({"code": "unauthorized", "message": "Unauthorized."}), status=401, content_type="application/json"
    )


# ---------------------------------------------------------------------------
# 엔드포인트
# ---------------------------------------------------------------------------
auth_bp = Blueprint("auth", __name__, url_prefix="/console/api")  # 로그인은 인증 전이므로 다른 blueprint
console_bp = Blueprint("console", __name__, url_prefix="/console/api")


@auth_bp.post("/login")
def login():
    body = request.get_json()
    account = next((a for a in ACCOUNTS.values() if a.email == body["email"]), None)
    if not account or account.password != body["password"]:  # Dify 는 salt+hash 비교 (libs/password.py)
        return jsonify(code="invalid_credentials"), 401
    exp = datetime.now(UTC) + timedelta(minutes=60)
    token = PassportService().issue(
        {"user_id": account.id, "exp": exp, "iss": "SELF_HOSTED", "sub": "Console API Passport"}
    )
    return jsonify(result="success", data={"access_token": token})


@console_bp.get("/account/profile")
@login_required
def profile():
    return jsonify(id=current_user.id, email=current_user.email, tenant_id=current_user.current_tenant_id)


def main() -> None:
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(console_bp)
    login_manager.init_app(app)

    @app.errorhandler(Unauthorized)
    def _401(e):
        return jsonify(code="unauthorized", message=e.description), 401

    c = app.test_client()

    print("토큰 없이     ->", c.get("/console/api/account/profile").get_json())

    r = c.post("/console/api/login", json={"email": "admin@example.com", "password": "password123"})
    token = r.get_json()["data"]["access_token"]
    print("로그인        ->", r.status_code, token[:40] + "...")
    print("JWT payload   ->", jwt.decode(token, options={"verify_signature": False}))

    r = c.get("/console/api/account/profile", headers={"Authorization": f"Bearer {token}"})
    print("Bearer 토큰   ->", r.status_code, r.get_json())

    tampered = token[:-2] + ("aa" if token[-2:] != "aa" else "bb")
    r = c.get("/console/api/account/profile", headers={"Authorization": f"Bearer {tampered}"})
    print("변조 토큰     ->", r.status_code, r.get_json())

    expired = PassportService().issue({"user_id": "u1", "exp": datetime.now(UTC) - timedelta(seconds=1)})
    r = c.get("/console/api/account/profile", headers={"Authorization": f"Bearer {expired}"})
    print("만료 토큰     ->", r.status_code, r.get_json())


if __name__ == "__main__":
    main()
