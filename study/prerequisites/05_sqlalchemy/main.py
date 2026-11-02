"""SQLAlchemy 2.0 + Flask-SQLAlchemy 예제.

Dify 에서의 용도
  - api/models/engine.py : naming_convention 이 있는 MetaData 와 `db = SQLAlchemy(metadata=metadata)`
  - api/models/base.py   : Base(DeclarativeBase), TypeBase(MappedAsDataclass) — `Mapped[...]` 타입 힌트 스타일
  - api/models/types.py  : StringUUID 같은 TypeDecorator (PG 에선 UUID, 그 외엔 CHAR(36))
  - api/core/db/session_factory.py : sessionmaker 기반 세션 팩토리 (서비스 레이어에서 사용)
  - 쿼리는 2.0 스타일 `select(Model).where(...)` + `session.scalars()/scalar()` 를 쓴다.

여기서는 SQLite 메모리 DB 로 돌린다. (Dify 실제 DB 는 PostgreSQL/MySQL)
실행: uv run --project api python example/05_sqlalchemy/main.py
"""

import uuid
from datetime import UTC, datetime
from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CHAR, DateTime, ForeignKey, Index, MetaData, String, Text, func, select
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, Session, mapped_column, sessionmaker
from sqlalchemy.types import TypeDecorator

# ---------------------------------------------------------------------------
# 1) MetaData + naming convention (models/engine.py)
#    → 인덱스/제약조건 이름이 규칙적으로 생성되어 Alembic 마이그레이션이 안정적이다.
# ---------------------------------------------------------------------------
metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)
db = SQLAlchemy(metadata=metadata)


# ---------------------------------------------------------------------------
# 2) 커스텀 컬럼 타입 (models/types.py 의 StringUUID 단순화)
# ---------------------------------------------------------------------------
class StringUUID(TypeDecorator[str]):
    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(self, value: Any, dialect: Dialect) -> str | None:
        return None if value is None else str(value)


# ---------------------------------------------------------------------------
# 3) 모델 정의 — Mapped[] 타입 힌트 스타일 (models/base.py)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    metadata = metadata


class TypeBase(MappedAsDataclass, DeclarativeBase):
    """dataclass 처럼 생성자/repr 이 자동 생성되는 베이스 (Dify 신규 모델이 점진 이전 중)"""

    metadata = metadata


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(StringUUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())


class App(Base):
    __tablename__ = "apps"
    __table_args__ = (Index("app_tenant_id_idx", "tenant_id"),)

    id: Mapped[str] = mapped_column(StringUUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Dify 는 대부분 DB FK 를 걸지 않고 tenant_id 로 논리적 관계만 둔다. 여기선 학습용으로 FK 를 건다.
    tenant_id: Mapped[str] = mapped_column(StringUUID, ForeignKey("tenants.id"))
    name: Mapped[str] = mapped_column(String(255))
    mode: Mapped[str] = mapped_column(String(32), default="chat")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    @property
    def tenant(self) -> Tenant | None:
        # Dify 모델은 relationship() 대신 이런 property + 명시적 쿼리를 쓰는 경우가 많다
        return db.session.get(Tenant, self.tenant_id)


class Message(TypeBase):
    __tablename__ = "messages"

    app_id: Mapped[str] = mapped_column(StringUUID)
    query: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text, default="")
    id: Mapped[str] = mapped_column(StringUUID, primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default_factory=lambda: datetime.now(UTC))


def main() -> None:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_ECHO"] = False  # True 로 바꾸면 실행되는 SQL 이 보인다
    db.init_app(app)  # extensions/ext_database.py

    with app.app_context():
        db.create_all()  # 실제 Dify 는 create_all 대신 Flask-Migrate(Alembic) 로 스키마 관리 (06 예제)
        print("생성된 테이블:", list(metadata.tables))
        print("인덱스 이름 :", [ix.name for ix in App.__table__.indexes])

        # --- (a) Flask-SQLAlchemy 의 요청 범위 세션: db.session (controllers 에서 주로 사용)
        tenant = Tenant(name="Acme")
        db.session.add(tenant)
        db.session.flush()  # INSERT 는 보내되 커밋 전 → id 사용 가능
        db.session.add_all(
            [
                App(tenant_id=tenant.id, name="Support Bot", mode="chat"),
                App(tenant_id=tenant.id, name="Summarizer", mode="workflow"),
            ]
        )
        db.session.commit()

        # 2.0 스타일 쿼리
        stmt = select(App).where(App.tenant_id == tenant.id, App.mode == "chat").order_by(App.name)
        chat_apps = db.session.scalars(stmt).all()
        print("\nchat 앱:", [(a.name, a.tenant.name) for a in chat_apps])

        count = db.session.scalar(select(func.count()).select_from(App).where(App.tenant_id == tenant.id))
        print("앱 개수:", count)

        # JOIN
        rows = db.session.execute(select(App.name, Tenant.name).join(Tenant, App.tenant_id == Tenant.id)).all()
        print("JOIN 결과:", rows)

        # --- (b) sessionmaker 세션 팩토리 (core/db/session_factory.py) — 서비스/태스크에서 사용
        session_maker = sessionmaker(bind=db.engine, expire_on_commit=False)
        with session_maker() as session, session.begin():  # begin(): 블록 끝에서 자동 commit / 예외 시 rollback
            msg = Message(app_id=chat_apps[0].id, query="안녕?", answer="안녕하세요!")
            session.add(msg)
        print("\nMessage(dataclass 모델):", msg)

        try:
            with Session(db.engine) as session, session.begin():
                session.add(Message(app_id=chat_apps[0].id, query="롤백될 메시지"))
                raise RuntimeError("중간에 실패")
        except RuntimeError:
            pass
        with Session(db.engine) as session:
            print("롤백 후 메시지 수:", session.scalar(select(func.count()).select_from(Message)))


if __name__ == "__main__":
    main()
