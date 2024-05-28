import os
from datetime import datetime, timedelta

import requests

import crdt.speasy as sp

SERVER_URL = os.environ["SERVER_URL"]
assert SERVER_URL


def get_request(path, headers={}):
    req = requests.get(SERVER_URL + path, headers=headers)
    req.raise_for_status()
    return req


def post_request(path, data=None, json=None):
    assert not (data and json)
    req = requests.post(SERVER_URL + path, data=data, json=json)
    req.raise_for_status()
    return req


def main():
    req = post_request("/create_catalogue", json={"name": "catalogue_xyz"})
    catalogue_id = req.json()["doc_id"]
    event = sp.Event(
        start=datetime.now() - timedelta(days=356),
        stop=datetime.now() - timedelta(days=356) + timedelta(days=1),
        author="jeandet",
        tags=[],
        products=[],
        rating="none",
        uuid=sp.uuid(),
    )
    req = post_request(f"/add_event/{catalogue_id}", data=event.json())

    print(get_request(f"/get_events/{catalogue_id}").json())

    req = post_request(
        f"/edit_event/{catalogue_id}/{event.uuid}", json=dict(author="banana")
    )
    print(get_request(f"/get_events/{catalogue_id}").json())


if __name__ == "__main__":
    main()
