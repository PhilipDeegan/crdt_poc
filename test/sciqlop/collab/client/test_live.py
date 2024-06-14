# https://websocket-client.readthedocs.io/en/latest/examples.html
# https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app
#
# needs:
#  pip install websocket-client
#

import json
import time
from datetime import datetime, timedelta
from threading import Thread

import sciqlop.collab.client.client as client
import sciqlop.collab.client.keyboard as kb
import sciqlop.collab.crdt.manager as cdrt_man
import sciqlop.collab.model.speasy_model as sp_model
import sciqlop.collab.server.speasy_ws_api as sp_api

_globals = dict(poller=None, response_id=1000)
client_id = "client_1234"
WS_URL = f"ws://localhost:8000/ws/{client_id}"
on_open_fn = None
catalogue_name = "test_catalogue_123"


def test_create_catalogue():
    _globals["response_id"] = 0
    return sp_api.CreateCatalogueRequest(name=catalogue_name)


def test_create_event():
    _globals["response_id"] = 1
    return sp_api.CreateEventRequest(
        catalogue_uuid=_globals["catalogue_uuid"],
        event=sp_model.Event(
            start=datetime.now() - timedelta(days=356),
            stop=datetime.now() - timedelta(days=356) + timedelta(days=1),
            author="jeandet",
            tags=[],
            products=[],
            rating="none",
            uuid=cdrt_man.uuid(),
        ),
    )


def test_edit_event():
    _globals["response_id"] = 2
    return sp_api.EditEventRequest(
        catalogue_uuid=_globals["catalogue_uuid"],
        event_uuid=_globals["event_uuid"],
        dic=dict(author="bananaman"),
    )


def test_list_events():
    _globals["response_id"] = 3
    return sp_api.ListEventsRequest(catalogue_uuid=_globals["catalogue_uuid"])


test_events = {
    "cc": test_create_catalogue,
    "create_catalogue": test_create_catalogue,
    "ce": test_create_event,
    "create_event": test_create_event,
    "ee": test_edit_event,
    "edit_event": test_edit_event,
    "le": test_list_events,
    "list_events": test_list_events,
}


def resolve_event(txt):
    if txt in client.events:
        return client.events[txt]()
    if txt in test_events:
        return test_events[txt]()


def handle_keyboard_input():
    event = resolve_event(kb.poll())
    if not event:
        print("event not recognized")
        time.sleep(1)
        return
    print("event", event)
    client.send(event)


def poll():
    """simulate some event loop"""
    while True:
        handle_keyboard_input()


def on_open(wsapp):
    try:
        _globals["poller"] = Thread(target=poll)
        _globals["poller"].daemon = True
        _globals["poller"].start()
    except Exception as e:
        print(f"EXCEPTION! {e}")


def create_catalogue_response(wsapp, msg):
    try:
        print("create_catalogue_response", msg)
        resp = sp_api.CreateCatalogueResponse(**json.loads(msg))
        _globals["catalogue_uuid"] = resp.catalogue_uuid
    except Exception as e:
        print(f"EXCEPTION! {e}")


def create_event_response(wsapp, msg):
    try:
        print("create_event_response", msg)
        resp = sp_api.CreateEventResponse(**json.loads(msg))
        _globals["event_uuid"] = resp.event_uuid
    except Exception as e:
        print(f"EXCEPTION! {e}")


def edit_event_response(wsapp, msg):
    print("edit_event_response", msg)


def list_events_response(wsapp, msg):
    print("list_events_response", msg)


response_mappers = {
    0: create_catalogue_response,
    1: create_event_response,
    2: edit_event_response,
    4: list_events_response,
}


def on_message(wsapp, msg):
    response_id = _globals["response_id"]
    if response_id in response_mappers:
        response_mappers[_globals["response_id"]](wsapp, msg)
    else:
        print(msg)


if __name__ == "__main__":
    client.on_open_fn = on_open
    client.on_message_fn = on_message
    client.start(WS_URL).join()
