import random
import string
from dataclasses import dataclass, field
from datetime import datetime

from pycrdt import Array, ArrayEvent, Doc, Map, TransactionEvent
from pydantic import BaseModel

alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
_GLOBALS = dict(docs={})


# https://jupyter-server.github.io/pycrdt/usage/#shared-data-events
def handle_deep_changes(events: list[ArrayEvent]):
    ... # haven't seen this trigger yet
    #
    #print("handle_deep_changes")


def handle_doc_changes(event: TransactionEvent):
    # Triggers on:
    #   event creation
    #   event edit
    # Does not trigger on catalog creation!
    # print("\n\nhandle_doc_changes")
    # update: bytes = event.update


class Event(BaseModel):
    start: datetime
    stop: datetime
    author: str
    tags: list
    products: list
    rating: str
    uuid: str

    # @staticmethod
    # def from_dict(dic: dict[str, str]):
    #     return Event(
    #         start=datetime.fromisoformat(dic["start"]),
    #         stop=datetime.fromisoformat(dic["stop"]),
    #         author=dic["author"],
    #         tags=dic["tags"],
    #         products=dic["products"],
    #         rating=dic["rating"],
    #         uuid=dic["uuid"],
    #     )


@dataclass  # crdt doesn't play well with pydantic
class Document:
    name: str
    uuid: str
    events_to_idx: dict = field(default_factory=lambda: {})
    events: Array = field(default_factory=lambda: Array())
    doc: Doc = field(default_factory=lambda: Doc())

    def __post_init__(self):
        self.doc["events"] = self.events
        self.doc.observe(handle_doc_changes)


def uuid(k=8):
    return "".join(random.choices(alphabet, k=k))


def create_document(name):
    doc = Document(name=name, uuid=uuid())
    _GLOBALS["docs"][doc.uuid] = doc
    return doc


def resolve_crdt_type_for(v):
    if isinstance(v, list):
        return Array([i for i in v])
    return str(v)


def add_event(doc_id, event):
    doc = _GLOBALS["docs"][doc_id]
    doc.events_to_idx[event.uuid] = len(doc.events)  # needs mutex?
    doc.events.append(
        Map({k: resolve_crdt_type_for(v) for k, v in event.dict().items()})
    )


def edit_event(doc_id, event_id, dic):
    doc = _GLOBALS["docs"][doc_id]
    doc.events[doc.events_to_idx[event_id]].update(dic)


def resolve_regular_for(v):
    if isinstance(v, Array):
        return [i for i in v]
    return v


def get_events(doc_id):
    return [
        Event(**{k: resolve_regular_for(v) for k, v in ev.items()})
        for ev in _GLOBALS["docs"][doc_id].events
    ]
