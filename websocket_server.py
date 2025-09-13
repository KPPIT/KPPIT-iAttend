import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio, random
from datetime import datetime

app = FastAPI()

def get_live_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "value": round(random.uniform(10, 100), 2)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(get_live_data())
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
