# https://websocket-client.readthedocs.io/en/latest/examples.html
# https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app
#
# needs:
#  pip install websocket-client
#

import atexit
import signal
import sys
import time
from typing import Callable

import websocket

# import sciqlop.collab.model.speasy_model as sp_model
import sciqlop.collab.server.speasy_ws_api as sp_api

_globals = dict(client=None)
client_str = "client"
on_open_fn: Callable | None = None
on_message_fn: Callable | None = None
events = {
    "list": sp_api.ListCataloguesRequest,
    "update": None,
    "create": None,
    "edit": None,
}


# def signal_handler(sig, frame):
#     shutdown()


signal.signal(signal.SIGINT, lambda s, f: shutdown())


@atexit.register
def shutdown():
    if _globals[client_str]:
        print("shutting down")
        # client.send("Bye, Server")
        _globals[client_str] = None
        time.sleep(1)
        sys.exit()


def on_open(wsapp):
    try:
        if on_open_fn and isinstance(on_open_fn, Callable):
            on_open_fn(wsapp)
    except Exception as e:
        print(f"EXCEPTION! {e}")


def on_close(wsapp, status, message):
    print("on_close", status, message)
    # wsapp.send("Bye, Server")
    _globals[client_str] = None


def on_message(wsapp, message):
    print("on_message")
    if on_message_fn and isinstance(on_message_fn, Callable):
        on_message_fn(wsapp, message)


def start(url):
    _globals[client_str] = websocket.WebSocketApp(
        url, on_open=on_open, on_message=on_message, on_close=on_close
    )
    return sys.modules[__name__]


def join():
    client = _globals[client_str]
    if not client:
        raise RuntimeError("No active client")
    client.run_forever()


def stop():
    shutdown()


def send(obj):
    client = _globals[client_str]
    if not client:
        raise RuntimeError("No active client")
    msg = sp_api.RequestWrapper(type=type(obj).__name__, data=obj)
    print("msg", msg.json())
    client.send(msg.json())
