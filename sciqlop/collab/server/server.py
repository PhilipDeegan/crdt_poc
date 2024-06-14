# import os
# from datetime import datetime, timedelta

import json
import traceback

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import sciqlop.collab.server.actions as actions
import sciqlop.collab.server.connection_manager as con_man
import sciqlop.collab.server.speasy_ws_api as sp_api

# import sciqlop.collab.model.speasy_model as sp_model

app = FastAPI()
manager = con_man.ConnectionManager()
available_requests = sp_api.available_requests
available_actions = actions.available_actions


def handle_request(data):
    try:
        dic = json.loads(data)
        if "type" not in dic or "data" not in dic:
            print("Unknown request type")
            return
        req_type = dic["type"]
        if req_type not in available_requests:
            print(f"Unknown request type: {req_type}")
            return
        req_type = available_requests[req_type]
        print("req_type", req_type)
        return available_actions[req_type](req_type(**dic["data"]))
    except Exception as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        return data


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await websocket.send_json({"msg": "Hello WebSocket"})

    try:
        while True:
            data = await websocket.receive_text()
            print("received: ", data)

            response = handle_request(data)
            if not response:
                continue
            await manager.send_personal_message(response.json(), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
