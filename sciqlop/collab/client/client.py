# https://websocket-client.readthedocs.io/en/latest/examples.html
# https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app
#
# needs:
#  pip install websocket-client
#
import atexit
import signal
import sys
import traceback
from typing import Callable

import websocket

# import sciqlop.collab.model.speasy_model as sp_model
import sciqlop.collab.server.speasy_ws_api as sp_api

_globals = dict(client=None)
reraise = False
client_str = "client"
on_open_fn: Callable | None = None
on_message_fn: Callable | None = None
events = {
    "list": sp_api.ListCataloguesRequest,
    "update": None,
    "create": None,
    "edit": None,
}


signal.signal(signal.SIGINT, lambda s, f: shutdown())


@atexit.register
def shutdown():
    if _globals[client_str]:
        print("shutting down")
        # client.send("Bye, Server")
        _globals[client_str].close()
        _globals[client_str] = None


def on_open(wsapp):
    try:
        if on_open_fn and isinstance(on_open_fn, Callable):
            on_open_fn(wsapp)
    except Exception as e:
        print(f"on_open EXCEPTION! {e}")
        print(traceback.format_exc())
        if reraise:
            raise e


def on_close(wsapp, status, message):
    # maybe needs callback fn too
    print("on_close", status, message)
    _globals[client_str] = None


def on_message(wsapp, message):
    try:
        if on_message_fn and isinstance(on_message_fn, Callable):
            on_message_fn(wsapp, message)
    except Exception as e:
        print(f"on_message EXCEPTION! {e}")
        print(traceback.format_exc())
        if reraise:
            raise e


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


def send(obj):
    client = _globals[client_str]
    if not client:
        raise RuntimeError("No active client")
    msg = sp_api.MessageWrapper.make(obj)
    client.send(msg.json())
