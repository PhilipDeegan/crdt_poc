#
#
#


import json
import traceback

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import sciqlop.collab.server.actions as actions
import sciqlop.collab.server.speasy_ws_api as sp_api
from sciqlop.collab.server.connection_manager import ConnectionManager

app = FastAPI()
conn_man = ConnectionManager()


def handle_request(data):
    try:
        dic = json.loads(data)
        keys = list(dic.keys())
        if len(keys) != 1 or keys[0] not in sp_api.available_requests:
            return sp_api.ErrorResponse.status_code(400)
        req_type, req_data = sp_api.available_requests[keys[0]], dic[keys[0]]
        return sp_api.MessageWrapper.make(
            actions.available_actions[req_type](req_type(**req_data))
        )
    except Exception as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
    return sp_api.ErrorResponse.status_code(404)


@app.get("/ping")
def ping():
    return 200


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await conn_man.connect(client_id, websocket)
    # await websocket.send_json({"msg": "Hello WebSocket"})
    # send some conenection established message? not sure redundant

    try:
        while True:
            data = await websocket.receive_text()
            response = handle_request(data)
            if not response:
                continue
            await conn_man.send(response.json(), websocket)
            # if shared_resource:
            #   await conn_man.send_shared(response.json(), shared_resource.client_ids)

    except WebSocketDisconnect:
        conn_man.disconnect(client_id, websocket)
        await conn_man.broadcast(f"Client #{client_id} left the chat")
