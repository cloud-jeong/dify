## /console/api/login 호출시 실행 순서

1. app_factory.py의 before_request()가 모든 공통 입구임.
   WebSocketHandler -> socketio_app -> app_factory.py의 before_request()

2. login은 api/controllers/auth/login.pydml LoginAPI()함수이고 위에 decorator 순으로 먼저 실행됨.
   decorator는 api/controllers/console/wraps.py임.

```python
@console_ns.route("/login")
class LoginApi(Resource):
    """Resource for user login."""

    @error_responses(               // OpenAPI 오류 목록 문서화용
        AccountBannedError,
        AccountInFreezeError,
        AccountNotFound,
        AuthenticationFailedError,
        EmailDomainSuspendedError,
        EmailPasswordLoginLimitError,
        InvalidAccountPasswordRequestError,
        InvalidEmailError,
        WorkspacesLimitExceeded,
    )
    @setup_required                 // 초기 설치 후 관리자 생성이 끝났는지 확인
    @email_password_login_enabled   // 이메일, 비밀번호 로그인 방식이 on되어 있는지 확인 (SystemFeatureService)
    @console_ns.expect(console_ns.models[LoginPayload.__name__])    // 문서화용
    @console_ns.response(200, "Success", console_ns.models[SimpleResultOptionalDataResponse.__name__]) // 문서화용
    @decrypt_password_field         // 비밀번호 암호화가 on되어 있으면 요청의 password를 복호화
    @model_validate(LoginPayload)   // JSON 본문을 pydantic LoginPayLoad로 검증해서 req_data 로 주입
    def post(self, req_data: LoginPayload):
```
