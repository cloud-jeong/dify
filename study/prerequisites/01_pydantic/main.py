"""Pydantic v2 + pydantic-settings 예제.

Dify 에서의 용도
  1) 설정 관리:  api/configs/app_config.py 의 `DifyConfig`
     - 기능별 BaseSettings 클래스(DatabaseConfig, RedisConfig ...)를 다중 상속으로 합쳐
       하나의 전역 객체 `dify_config` 를 만든다.
     - 값은 환경변수 / .env 파일에서 자동으로 읽고 타입 검증한다.
  2) 요청/응답 스키마: controllers/** 의 Payload / Response 모델 (BaseModel + model_validate)

실행: uv run --project api python example/01_pydantic/main.py
"""

import os
from enum import StrEnum

from pydantic import BaseModel, Field, PositiveInt, ValidationError, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# 1) 설정: 기능별로 쪼갠 BaseSettings → 다중 상속으로 합치기 (DifyConfig 패턴)
# ---------------------------------------------------------------------------
class DatabaseConfig(BaseSettings):
    DB_HOST: str = Field(default="localhost", description="DB host")
    DB_PORT: PositiveInt = Field(default=5432, description="DB port")
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = ""
    DB_DATABASE: str = "dify"

    # computed_field: 다른 필드로부터 계산되는 값 (configs/middleware/__init__.py 의 SQLALCHEMY_DATABASE_URI)
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802 (Dify 설정 키 컨벤션: 대문자)
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


class RedisConfig(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: PositiveInt = 6379
    REDIS_DB: int = Field(default=0, ge=0, le=15)


class DeploymentEdition(StrEnum):
    SELF_HOSTED = "SELF_HOSTED"
    CLOUD = "CLOUD"


class DeploymentConfig(BaseSettings):
    EDITION: DeploymentEdition = DeploymentEdition.SELF_HOSTED
    DEBUG: bool = False


class DemoConfig(DeploymentConfig, DatabaseConfig, RedisConfig):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# ---------------------------------------------------------------------------
# 2) 요청 페이로드 검증 (controllers/console/app/app.py 의 CreateAppPayload 패턴)
# ---------------------------------------------------------------------------
class AppMode(StrEnum):
    CHAT = "chat"
    WORKFLOW = "workflow"
    AGENT_CHAT = "agent-chat"


class CreateAppPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=40)
    mode: AppMode
    description: str | None = Field(default=None, max_length=400)
    icon: str = "🤖"

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be blank")
        return v


class AppResponse(BaseModel):
    id: str
    name: str
    mode: AppMode


def main() -> None:
    print("== 1) Settings ==")
    # 환경변수가 기본값을 덮어쓴다. 문자열 "6380" 도 int 로 변환·검증된다.
    os.environ["REDIS_PORT"] = "6380"
    os.environ["DEBUG"] = "true"
    os.environ["EDITION"] = "CLOUD"
    config = DemoConfig()
    print("REDIS_PORT =", config.REDIS_PORT, type(config.REDIS_PORT).__name__)
    print("DEBUG      =", config.DEBUG)
    print("EDITION    =", config.EDITION)
    print("DB URI     =", config.SQLALCHEMY_DATABASE_URI)

    os.environ["REDIS_DB"] = "99"
    try:
        DemoConfig()
    except ValidationError as e:
        print("잘못된 설정은 기동 시점에 실패:", e.errors()[0]["msg"])
    del os.environ["REDIS_DB"]

    print("\n== 2) Request payload ==")
    payload = CreateAppPayload.model_validate({"name": "  My Bot  ", "mode": "chat"})
    print("검증 통과:", payload)
    print("model_dump:", payload.model_dump(exclude_none=True))

    try:
        CreateAppPayload.model_validate({"name": "", "mode": "unknown"})
    except ValidationError as e:
        for err in e.errors():
            print("검증 실패:", err["loc"], err["msg"])

    print("\n== 3) Response 직렬화 + JSON Schema (Swagger 문서 생성에 사용) ==")
    resp = AppResponse(id="a1", name=payload.name, mode=payload.mode)
    print(resp.model_dump_json())
    print(AppResponse.model_json_schema())


if __name__ == "__main__":
    main()
