"""Flask-Migrate (Alembic) 예제 — DB 스키마 버전 관리.

Dify 에서의 용도
  - api/extensions/ext_migrate.py : Migrate(app, db) 등록
  - api/migrations/versions/*.py  : 수백 개의 리비전 파일 (upgrade()/downgrade())
  - 개발 흐름
      1) models/*.py 수정
      2) uv run --project api flask db revision --autogenerate -m "add xxx"   (리비전 생성)
      3) uv run --project api flask db upgrade                                (적용)
    Docker 배포에서는 MIGRATION_ENABLED=true 이면 api 컨테이너 기동 시 자동 upgrade 한다 (api/docker/entrypoint.sh).

이 예제는 임시 디렉터리에서 CLI 대신 flask_migrate 파이썬 API 로 같은 흐름을 재현한다.
실행: uv run --project api python example/06_flask_migrate/main.py
"""

import logging
import tempfile
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate, downgrade, init, migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, String, inspect
from sqlalchemy.orm import Mapped, mapped_column

logging.getLogger("alembic").setLevel(logging.WARNING)


def build_app(workdir: Path, with_description: bool) -> tuple[Flask, SQLAlchemy]:
    """모델 정의가 바뀌는 상황을 흉내내기 위해 매번 새 app/db/모델을 만든다."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{workdir / 'demo.db'}"
    db = SQLAlchemy(metadata=MetaData())

    class App(db.Model):  # type: ignore[name-defined]
        __tablename__ = "apps"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(255))
        if with_description:
            description: Mapped[str | None] = mapped_column(String(400), nullable=True)

    db.init_app(app)
    Migrate(app, db, directory=str(workdir / "migrations"))
    return app, db


def show(app: Flask, db: SQLAlchemy, title: str) -> None:
    with app.app_context():
        insp = inspect(db.engine)
        cols = [c["name"] for c in insp.get_columns("apps")] if insp.has_table("apps") else "(테이블 없음)"
        print(f"{title:<28} apps 컬럼 = {cols}")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        # --- v1 모델
        app, db = build_app(workdir, with_description=False)
        with app.app_context():
            init()  # = flask db init  → migrations/ 폴더(alembic.ini, env.py, versions/) 생성
            migrate(message="create apps")  # = flask db migrate (autogenerate)
            upgrade()  # = flask db upgrade
        show(app, db, "v1 upgrade 후")

        # --- v2 모델: 컬럼 추가
        app, db = build_app(workdir, with_description=True)
        with app.app_context():
            migrate(message="add description to apps")
            upgrade()
        show(app, db, "v2 upgrade 후")

        versions = sorted((workdir / "migrations" / "versions").glob("*.py"), key=lambda p: p.stat().st_mtime)
        print("\n생성된 리비전 파일:")
        for v in versions:
            print("  ", v.name)
        print("\n마지막 리비전 내용 (upgrade/downgrade 부분):")
        body = versions[-1].read_text()
        print(body[body.index("def upgrade") :])

        # --- 되돌리기
        with app.app_context():
            downgrade()  # = flask db downgrade  (한 단계)
        show(app, db, "downgrade 1 단계 후")


if __name__ == "__main__":
    main()
