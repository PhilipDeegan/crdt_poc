import random
import string
from dataclasses import dataclass, field

from pycrdt import Array, ArrayEvent, Doc, Map, TransactionEvent

import sciqlop.collab.model.speasy_model as sp_model

# from datetime import datetime


alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
_GLOBALS = dict(catalogues={})


# https://jupyter-server.github.io/pycrdt/usage/#shared-data-events
def handle_deep_changes(events: list[ArrayEvent]):
    print("\n\nhandle_deep_changes")


def handle_doc_changes(event: TransactionEvent):
    print("\n\nhandle_doc_changes")
    # update: bytes = event.update


@dataclass
class Catalogue:
    name: str
    uuid: str
    events_to_idx: dict = field(default_factory=lambda: {})
    events: Array = field(default_factory=lambda: Array())
    doc: Doc = field(default_factory=lambda: Doc())

    def __post_init__(self):
        self.doc["events"] = self.events
        self.doc.observe(handle_doc_changes)

    def info(self):
        return {"name": self.name, "uuid": self.uuid}


def uuid(k=8):
    return "".join(random.choices(alphabet, k=k))


def create_catalogue(name):
    doc = Catalogue(name=name, uuid=uuid())
    _GLOBALS["catalogues"][doc.uuid] = doc
    return doc


def list_catalogues():
    return [c.info() for c in _GLOBALS["catalogues"]]


def list_events(catalogue_uuid: str):
    return get_events(catalogue_uuid)


def resolve_crdt_type_for(v):
    if isinstance(v, list):
        return Array([i for i in v])
    return str(v)


def create_event(doc_id, event):
    doc = _GLOBALS["catalogues"][doc_id]
    doc.events_to_idx[event.uuid] = len(doc.events)  # needs mutex?
    doc.events.append(
        Map({k: resolve_crdt_type_for(v) for k, v in event.dict().items()})
    )
    return event


def edit_event(doc_id, event_id, dic):
    doc = _GLOBALS["catalogues"][doc_id]
    doc.events[doc.events_to_idx[event_id]].update(dic)


def resolve_regular_for(v):
    if isinstance(v, Array):
        return [i for i in v]
    return v


def get_events(doc_id):
    return [
        sp_model.Event.from_dict({k: resolve_regular_for(v) for k, v in ev.items()})
        for ev in _GLOBALS["catalogues"][doc_id].events
    ]
