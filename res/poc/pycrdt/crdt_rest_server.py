from fastapi import FastAPI
from pydantic import BaseModel

import crdt.speasy_crdt_api as sp

app = FastAPI()


class CreateCatalogueRequest(BaseModel):
    name: str


@app.post("/create_catalogue")
async def create(req: CreateCatalogueRequest):
    doc = sp.create_document(req.name)
    return {"message": "/create_catalog", "doc_id": doc.uuid}


@app.post("/add_event/{doc_id}")
async def add_event(doc_id, event: sp.Event):
    sp.add_event(doc_id, event)
    return {"message": "/add_event", "event_id": event.uuid}


@app.post("/edit_event/{doc_id}/{event_id}")
async def edit_event(doc_id, event_id, req: dict):
    sp.edit_event(doc_id, event_id, req)
    return {"message": "/edit_event"}


@app.get("/init")
async def init():
    return {"message": "Hello World"}


@app.get("/poll/{unix_time}")
async def poll(unix_time: int):
    return {"message": "Hello World"}


@app.get("/get_catalogs")
async def get_catalogs():  # user session?
    return {"message": "Hello World"}


@app.get("/get_events/{doc_id}")
async def get_events(doc_id):
    return sp.get_events(doc_id)
    # return {"message": "Hello World"}


@app.get("/get_update/{doc_id}/{event_id}")
async def get_update(doc_id, event_id):
    return {"message": "Hello World"}
