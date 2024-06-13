# https://websocket-client.readthedocs.io/en/latest/examples.html
# https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app
#
# needs:
#  pip install websocket-client
#


import sys
import time
import atexit
import signal
import websocket
from threading import Thread


_globals = dict(client=None, poller=None)
client_str = "client"
client_id = "client_id_1234"  # will be input
WS_URL = f"ws://localhost:8000/ws/{client_id}"


def signal_handler(sig, frame):
    shutdown()


signal.signal(signal.SIGINT, signal_handler)


@atexit.register
def shutdown():
    if client := _globals[client_str]:
        print("shutting down")
        client.send("Bye, Server")
        _globals[client_str] = None
        time.sleep(1)
        sys.exit()


def poll():
    """ simulate some event loop """
    while True:
        time.sleep(5)
        wsapp.send("Poll, Server")


def on_open(wsapp):
    try:
        wsapp.send("Hello, Server")
        _globals["poller"] = Thread(target=poll)
        _globals["poller"].daemon = True
        _globals["poller"].start()
    except Exception as e:
        print(f"EXCEPTION! {e}")


def on_close(wsapp, status, message):
    print("on_close", status, message)
    wsapp.send("Bye, Server")
    _globals["client_str"] = None
    _globals["poller"] = None


def on_message(wsapp, message):
    print("on_message", message)
    # wsapp.send("Hello, Server") # bad!


_globals[client_str] = wsapp = websocket.WebSocketApp(
    WS_URL, on_open=on_open, on_message=on_message, on_close=on_close
)

wsapp.run_forever()
