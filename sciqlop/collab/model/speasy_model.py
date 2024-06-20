from datetime import datetime

from pydantic import BaseModel, Field


class Catalogue(BaseModel):
    uuid: str
    name: str


class Product(BaseModel):
    uuid: str
    name: str


class Event(BaseModel):
    start: datetime
    stop: datetime
    author: str
    rating: str
    uuid: str
    products: list[Product] = Field(default_factory=[])
    tags: list[str] = Field(default_factory=[])

    # @staticmethod
    # def from_dict(dic: dict[str, str]):
    #     return Event(**dic)
