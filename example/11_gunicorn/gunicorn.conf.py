"""gunicorn 설정 파일 (Dify: api/gunicorn.conf.py).

gunicorn 은 -c 로 지정한 이 파일을 "monkey patch 전에" 로드한다.
그래서 patch 이후 해야 할 추가 작업은 gevent 이벤트 구독으로 미룬다.
(Dify 는 여기서 grpc.experimental.gevent.init_gevent(), psycogreen.patch_psycopg() 를 호출)
"""

from gevent import events as gevent_events


def post_patch(event):
    if not isinstance(event, gevent_events.GeventDidPatchBuiltinModulesEvent):
        return
    print("[gunicorn.conf] stdlib patched by gevent → 여기서 psycopg2/grpc 추가 패치", flush=True)


gevent_events.subscribers.append(post_patch)

loglevel = "warning"
