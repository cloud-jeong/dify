"""python-socketio 예제 — 워크플로 실시간 협업(방/브로드캐스트).

Dify 에서의 용도
  - api/extensions/ext_socketio.py
      sio = socketio.Server(async_mode="gevent", client_manager=socketio.RedisManager(...))
      RedisManager: API 워커/파드가 여러 개여도 Redis Pub/Sub 으로 방(room) 이벤트를 공유
  - api/app_factory.py : socketio_app = socketio.WSGIApp(sio, flask_app)  → gunicorn 이 이걸 서빙
  - api/controllers/console/socketio/workflow.py
      connect            : 토큰(JWT) 검증 → 실패 시 False 반환하여 연결 거부
      user_connect       : workflow_id 방에 입장 (리더 선출)
      collaboration_event: mouse_move / workflow_update / comments_update ... 를 같은 방의 다른 사용자에게 relay
      graph_event        : 그래프 변경 브로드캐스트

이 예제는 Dify 와 같은 gevent 모드(gevent-websocket 서버)로 서버를 띄우고, 클라이언트 2개(Alice, Bob)가
같은 워크플로 방에서 이벤트를 주고받는다. (--redis 옵션을 주면 Dify 처럼 RedisManager 사용)
실행: uv run --project api python example/13_socketio/main.py [--redis]
"""

from gevent import monkey

monkey.patch_all()

import os
import sys

import gevent
import socketio
from flask import Flask
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

VALID_TOKENS = {"token-alice": "alice", "token-bob": "bob"}  # Dify: PassportService().verify(token)
REDIS_URL = os.getenv("REDIS_URL", "redis://:difyai123456@localhost:6379/15")

client_manager = socketio.RedisManager(REDIS_URL, channel="example-socketio") if "--redis" in sys.argv else None
sio = socketio.Server(async_mode="gevent", client_manager=client_manager, cors_allowed_origins="*")
flask_app = Flask(__name__)
app = socketio.WSGIApp(sio, flask_app)  # HTTP 는 Flask 로, /socket.io/ 는 Socket.IO 로


@sio.on("connect")
def on_connect(sid, environ, auth):
    user = VALID_TOKENS.get((auth or {}).get("token", ""))
    if not user:
        print(f"[server] 연결 거부 sid={sid}")
        return False  # 연결 거부
    sio.save_session(sid, {"user": user})
    print(f"[server] {user} 연결 sid={sid}")
    return True


@sio.on("user_connect")
def on_user_connect(sid, data):
    workflow_id = data.get("workflow_id")
    if not workflow_id:
        return {"msg": "workflow_id is required"}, 400
    user = sio.get_session(sid)["user"]
    room = f"workflow:{workflow_id}"
    sio.enter_room(sid, room)
    # 방의 다른 사람들에게 접속 알림 (skip_sid: 본인 제외)
    sio.emit("online_users", {"joined": user}, room=room, skip_sid=sid)
    return {"msg": "connected", "user_id": user, "sid": sid}  # ack(콜백) 응답


@sio.on("collaboration_event")
def on_collaboration_event(sid, data):
    user = sio.get_session(sid)["user"]
    for room in sio.rooms(sid):
        if room.startswith("workflow:"):
            sio.emit("collaboration_update", {**data, "from": user}, room=room, skip_sid=sid)
    return {"msg": "relayed"}


@sio.on("disconnect")
def on_disconnect(sid, *args):
    print(f"[server] disconnect sid={sid}")


def make_client(name: str) -> socketio.Client:
    c = socketio.Client()

    @c.on("online_users")
    def _online(data):
        print(f"  [{name}] online_users: {data}")

    @c.on("collaboration_update")
    def _update(data):
        print(f"  [{name}] collaboration_update: {data}")

    return c


def main() -> None:
    # gunicorn 의 GeventWebSocketWorker 가 내부적으로 하는 일과 같다
    server = pywsgi.WSGIServer(("127.0.0.1", 5198), app, handler_class=WebSocketHandler, log=None)
    server.start()
    url = "http://127.0.0.1:5198"

    print("== 1) 잘못된 토큰으로 연결 시도 ==")
    bad = socketio.Client()
    try:
        bad.connect(url, auth={"token": "wrong"}, transports=["websocket"])
    except socketio.exceptions.ConnectionError as e:
        print("  클라이언트: 연결 실패 →", e)

    print("\n== 2) Alice, Bob 연결 후 같은 워크플로 방 입장 ==")
    alice, bob = make_client("alice"), make_client("bob")
    alice.connect(url, auth={"token": "token-alice"}, transports=["websocket"])
    bob.connect(url, auth={"token": "token-bob"}, transports=["websocket"])
    print("  [alice] ack:", alice.call("user_connect", {"workflow_id": "wf-1"}))
    print("  [bob]   ack:", bob.call("user_connect", {"workflow_id": "wf-1"}))
    gevent.sleep(0.3)

    print("\n== 3) Alice 가 마우스 이동 / 노드 수정 이벤트 전송 → Bob 만 받음 ==")
    alice.emit("collaboration_event", {"type": "mouse_move", "data": {"x": 120, "y": 80}})
    alice.emit("collaboration_event", {"type": "workflow_update", "data": {"node_id": "llm-1", "title": "GPT"}})
    gevent.sleep(0.5)

    alice.disconnect()
    bob.disconnect()
    gevent.sleep(0.2)
    server.stop()


if __name__ == "__main__":
    main()
