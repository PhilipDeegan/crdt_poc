from datetime import datetime

from pydantic import BaseModel


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
    tags: list
    products: list[Product]
    rating: str
    uuid: str

    @staticmethod
    def from_dict(dic: dict[str, str]):
        return Event(
            start=datetime.fromisoformat(dic["start"]),
            stop=datetime.fromisoformat(dic["stop"]),
            author=dic["author"],
            tags=dic["tags"],
            products=dic["products"],
            rating=dic["rating"],
            uuid=dic["uuid"],
        )
