"""gunicorn 으로 띄울 WSGI 앱 (Dify: api/app.py 의 `socketio_app`)."""

import os
import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/slow")
def slow():
    time.sleep(1)  # LLM 응답 대기처럼 I/O 로 오래 걸리는 요청 (gevent 워커에서는 patch 되어 양보함)
    return jsonify(pid=os.getpid())
