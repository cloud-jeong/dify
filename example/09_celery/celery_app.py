"""Celery 앱 + 태스크 정의 (api/extensions/ext_celery.py, api/tasks/*.py 구조를 축소).

Dify 패턴
  - FlaskTask: 모든 태스크를 Flask app_context 안에서 실행 → 태스크에서도 db.session, dify_config 사용 가능
  - 브로커/결과 백엔드: Redis (CELERY_BROKER_URL, CELERY_BACKEND)
  - 큐 분리: dataset(문서 인덱싱), mail, workflow, app_deletion, ... → 무거운 작업이 가벼운 작업을 막지 않게
  - @shared_task(queue="mail") 로 태스크 선언, 호출부는 xxx_task.delay(...)
  - beat_schedule: 주기 작업(정리, 통계 등) — `celery -A app.celery beat` 프로세스가 스케줄링
"""

import os
import time
from datetime import timedelta

from celery import Celery, Task, shared_task
from celery.schedules import crontab
from flask import Flask, current_app

REDIS_URL = os.getenv("REDIS_URL", "redis://:difyai123456@localhost:6379/15")


def create_flask_app() -> Flask:
    app = Flask("celery_demo")
    app.config["APP_NAME"] = "Dify Celery Demo"
    return app


def init_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, broker=REDIS_URL, backend=REDIS_URL)
    celery_app.conf.update(
        result_expires=3600,
        broker_connection_retry_on_startup=True,
        task_default_queue="default",
        timezone="UTC",
        beat_schedule={
            # ext_celery.py 의 beat_schedule 처럼 설정 값에 따라 조건부로 등록한다
            "clean_embedding_cache": {"task": "celery_app.clean_cache_task", "schedule": crontab(hour="2", minute="0")},
            "heartbeat": {"task": "celery_app.heartbeat_task", "schedule": timedelta(minutes=5)},
        },
    )
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


flask_app = create_flask_app()
celery = init_celery(flask_app)


# ---------------------------------------------------------------------------
# 태스크 (api/tasks/*.py)
# ---------------------------------------------------------------------------
@shared_task(queue="mail")
def send_invite_mail_task(email: str) -> str:
    # app_context 안이므로 current_app 사용 가능 (Dify: mail, db.session 등)
    time.sleep(0.2)
    return f"[{current_app.config['APP_NAME']}] invite mail sent to {email}"


@shared_task(queue="dataset")
def document_indexing_task(dataset_id: str, document_ids: list[str]) -> dict:
    # 실제 Dify: 문서 파싱 → 청크 분할 → 임베딩 → 벡터 DB 저장 (tasks/document_indexing_task.py)
    for doc_id in document_ids:
        time.sleep(0.1)
    return {"dataset_id": dataset_id, "indexed": len(document_ids)}


@shared_task(queue="dataset", bind=True, max_retries=2, default_retry_delay=0)
def flaky_task(self, fail_times: int) -> str:
    if self.request.retries < fail_times:
        raise self.retry(exc=RuntimeError(f"temporary failure #{self.request.retries + 1}"))
    return f"succeeded after {self.request.retries} retries"


@shared_task
def clean_cache_task() -> None: ...


@shared_task
def heartbeat_task() -> None: ...
