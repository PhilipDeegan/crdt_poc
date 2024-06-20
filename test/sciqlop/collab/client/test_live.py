# https://websocket-client.readthedocs.io/en/latest/examples.html
# https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app
#
# needs:
#  pip install websocket-client
#
#

import json
import time
from datetime import datetime, timedelta
from threading import Thread

import sciqlop.collab.client.client as client
import sciqlop.collab.crdt.manager as cdrt_man
import sciqlop.collab.model.speasy_model as sp_model
import sciqlop.collab.server.speasy_ws_api as sp_api
from sciqlop import ValDict

_globals = ValDict(poller=None, req_id=0, resp_id=0, catalogue_uuid="", event_uuid="")
client_id = "client_1234"
WS_URL = f"ws://localhost:8000/ws/{client_id}"
catalogue_name = "test_catalogue_123"


test_events = {
    0: lambda: sp_api.CreateCatalogueRequest(name=catalogue_name),
    1: lambda: sp_api.CreateEventRequest(
        catalogue_uuid=_globals.catalogue_uuid,
        event=sp_model.Event(
            start=datetime.now() - timedelta(days=356),
            stop=datetime.now() - timedelta(days=356) + timedelta(days=1),
            author="jeandet",
            tags=[],
            products=[],
            rating="none",
            uuid=cdrt_man.uuid(),
        ),
    ),
    2: lambda: sp_api.ListEventsRequest(catalogue_uuid=_globals.catalogue_uuid),
    3: lambda: sp_api.EditEventRequest(
        catalogue_uuid=_globals.catalogue_uuid,
        event_uuid=_globals.event_uuid,
        dic=dict(author="bananaman"),
    ),
    4: lambda: sp_api.ListEventsRequest(catalogue_uuid=_globals.catalogue_uuid),
}


def poll():
    """simulate some event loop"""
    while True:
        if _globals.req_id not in test_events:
            # no more work to do
            break

        if _globals.req_id != _globals.resp_id:
            print("waiting for response...")
            time.sleep(1)
            continue

        print("sending message...")
        time.sleep(1)
        client.send(test_events[_globals.req_id]())
        _globals.req_id += 1
        time.sleep(2)  # wait for response


def on_open(wsapp):
    _globals.poller = Thread(target=poll)
    _globals.poller.daemon = True
    _globals.poller.start()


def create_catalogue_response(resp: sp_api.CreateCatalogueResponse):
    print("create_catalogue_response", resp)
    _globals.catalogue_uuid = resp.catalogue_uuid


def create_event_response(resp: sp_api.CreateEventResponse):
    print("create_event_response", resp)
    _globals.event_uuid = resp.event_uuid


def edit_event_response(resp: sp_api.EditEventResponse):
    print("edit_event_response", resp)


def list_events_response(resp: sp_api.ListEventsResponse):
    print("list_events_response", resp)


response_mappers = {
    0: create_catalogue_response,
    1: create_event_response,
    2: list_events_response,
    3: edit_event_response,
    4: list_events_response,
}


def parse_response(msg):
    dic = json.loads(msg)
    keys = list(dic.keys())
    return sp_api.available_responses[keys[0]](**dic[keys[0]])  # fail == issue


def on_message(wsapp, msg):
    response_mappers[_globals.resp_id](parse_response(msg))
    _globals.resp_id += 1
    if _globals.resp_id not in response_mappers:
        time.sleep(3)  # let thread finish
        client.shutdown()


if __name__ == "__main__":
    client.on_open_fn = on_open
    client.on_message_fn = on_message
    client.start(WS_URL).join()
    assert _globals.catalogue_uuid  # not none or length 0
    assert _globals.event_uuid
    print("finished")
