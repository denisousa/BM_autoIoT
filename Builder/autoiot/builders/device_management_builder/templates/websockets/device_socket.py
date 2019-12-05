from flask import request, Flask
from flask_socketio import Namespace, emit, SocketIO
import json
import paho.mqtt.client as mqtt

from threading import Lock

thread = None
thread_lock = Lock()

count = 0

def background_thread(_socketio : SocketIO, _current_app : Flask, _namespace):
    """Example of how to send server generated events to clients."""

{{websocket.background_thread_code}}

class {{websocket.name}}(Namespace):

    def __init__(self, app, namespace):
        super(Namespace, self).__init__(namespace)
        self.app = app

    def on_connect(self):
{{websocket.on_connect_code}}


    def on_disconnect(self):
{{websocket.on_disconnect_code}}