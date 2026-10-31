"""Celery 예제 실행기.

실행: uv run --project api python example/09_celery/main.py
  - 같은 프로세스 안에서 worker 를 띄우고(celery.contrib.testing.worker),
    API 쪽처럼 .delay() 로 태스크를 큐에 넣은 뒤 결과를 받아본다.
  - Redis 가 필요하다 (08_redis 예제의 '준비' 참고).

실제 Dify 처럼 별도 프로세스로 돌려보려면 (example/09_celery 디렉터리에서):
  uv run --project ../../api celery -A celery_app.celery worker -P gevent -c 4 -Q default,mail,dataset -l INFO
  uv run --project ../../api celery -A celery_app.celery beat -l INFO
Dify 실제 명령: api/docker/entrypoint.sh
  celery -A celery_entrypoint.celery worker -P ${WORKER_POOL} -Q dataset,mail,workflow,... (MODE=worker)
  celery -A app.celery beat                                                           (MODE=beat)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from celery.contrib.testing.worker import start_worker
from celery_app import celery, document_indexing_task, flaky_task, send_invite_mail_task


def main() -> None:
    print("== 0) eager 모드: 브로커 없이 즉시 실행 (단위 테스트에서 유용) ==")
    celery.conf.task_always_eager = True
    print(send_invite_mail_task.delay("eager@example.com").get())
    celery.conf.task_always_eager = False

    print("\n== 1) 실제 worker 기동 (queues: default, mail, dataset) ==")
    with start_worker(
        celery, pool="threads", concurrency=4, queues=["default", "mail", "dataset"], perform_ping_check=False
    ):
        # API 컨트롤러/서비스에서 하는 것과 동일: 즉시 반환되고 작업은 worker 가 처리
        r1 = send_invite_mail_task.delay("new.member@example.com")
        r2 = document_indexing_task.delay("dataset-1", ["doc-a", "doc-b", "doc-c"])
        r3 = flaky_task.delay(fail_times=2)
        print("enqueue 직후 상태:", r1.state, r2.state, r3.state, "(task id:", r1.id, ")")

        print("mail     →", r1.get(timeout=10))
        print("indexing →", r2.get(timeout=10))
        print("retry    →", r3.get(timeout=10))

        # apply_async: 큐/지연 실행 등을 세밀하게 지정
        r4 = send_invite_mail_task.apply_async(args=["later@example.com"], countdown=1, queue="mail")
        print("countdown=1s →", r4.get(timeout=10))

    print("\n== 2) beat 스케줄 (beat 프로세스가 이 표대로 태스크를 큐에 넣는다) ==")
    for name, entry in celery.conf.beat_schedule.items():
        print(f"  {name:<22} {entry['task']:<30} {entry['schedule']}")


if __name__ == "__main__":
    main()
