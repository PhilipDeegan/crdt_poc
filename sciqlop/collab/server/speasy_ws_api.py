# from typing import Generic
from typing import TypeVar

from pydantic import BaseModel, RootModel

import sciqlop.collab.model.speasy_model as sp_model

DataT = TypeVar("DataT", bound=BaseModel)


def get_classes():
    import inspect
    import sys

    clazzes = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            clazzes.append(obj)
    return clazzes


def response_for(cls):
    assert cls.__name__.endswith("Request")
    needle = cls.__name__[:-7]
    for rsp in available_responses.keys():
        assert rsp.__name__.endswith("Response")
        name = rsp.__name__
        s = name[:-8]
        if s == needle:
            return available_responses[rsp]
    raise RuntimeError(f"No response type found for: {cls}")


class MessageWrapper(RootModel[dict[str, BaseModel]]):
    root: dict[str, DataT]

    @classmethod
    def make(cls, data) -> "MessageWrapper":
        return cls({type(data).__name__: data})


class ErrorResponse(BaseModel):
    status_code: int

    @classmethod
    def status_code(cls, status_code):
        return cls(status_code=status_code)


class ListCataloguesRequest(BaseModel): ...


class ListCataloguesResponse(BaseModel):
    catalogues: list[sp_model.Catalogue]


class CreateCatalogueRequest(BaseModel):
    name: str


class CreateCatalogueResponse(BaseModel):
    catalogue_uuid: str


class ListEventsRequest(BaseModel):
    catalogue_uuid: str


class ListEventsResponse(BaseModel):
    events: list[sp_model.Event]


class CreateEventRequest(BaseModel):
    catalogue_uuid: str
    event: sp_model.Event


class CreateEventResponse(BaseModel):
    event_uuid: str


class EditEventRequest(BaseModel):
    catalogue_uuid: str
    event_uuid: str
    dic: dict[str, str]  # keys must match Event class members


class EditEventResponse(BaseModel): ...


available_requests = {
    cls.__name__: cls for cls in get_classes() if cls.__name__.endswith("Request")
}
available_responses = {
    cls.__name__: cls for cls in get_classes() if cls.__name__.endswith("Response")
}
