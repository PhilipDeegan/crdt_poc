#
# pylint: disable=E1102
#
from sqlalchemy import Identity  # https://stackoverflow.com/a/75421789/795574
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship

Base = declarative_base()
metadata = Base.metadata


class Catalogue(Base):
    __tablename__ = "catalogue"
    # common cols
    id = Column(Integer, Identity(start=100001, cycle=True), primary_key=True)
    uuid = Column(String(12), unique=True)
    created_datetime = Column(DateTime, default=func.now())

    # local cols
    name = Column(String(20))

    # def __repr__(self):
    #     return f"id: {self.id}, name: {self.name}"


class Product(Base):
    __tablename__ = "product"
    # common cols
    id = Column(Integer, Identity(start=100001, cycle=True), primary_key=True)
    uuid = Column(String(12), unique=True)
    created_datetime = Column(DateTime, default=func.now())

    # local cols
    name = Column(String(20))
    events = relationship("Event", back_populates="product")

    # def __repr__(self):
    #     return f"id: {self.id}, name: {self.name}"


class Event(Base):
    __tablename__ = "event"
    # common cols
    id = Column(Integer, Identity(start=100001, cycle=True), primary_key=True)
    uuid = Column(String(12), unique=True)
    created_datetime = Column(DateTime, default=func.now())

    # local cols
    start = Column(DateTime, default=func.now())
    stop = Column(DateTime, default=func.now())
    author = Column(String(20))

    product_id = mapped_column(ForeignKey("product.id"))
    product = relationship("Product", back_populates="events")

    # def __repr__(self):
    #     return f"id: {self.id}, name: {self.name}"
