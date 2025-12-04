from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from typing import List, Dict
import uvicorn
import json

app = FastAPI(title="RealTime Book Board")

# In-memory storage 
books: List[Dict] = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "David Thomas"},
    {"id": 2, "title": "Clean Architecture", "author": "Robert C. Martin"},
]

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def broadcast(self, message: dict):
        dead = []
        for conn in self.active_connections:
            try:
                await conn.send_json(message)
            except:
                dead.append(conn)
        for conn in dead:
            self.active_connections.remove(conn)

manager = ConnectionManager()

# HTML
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send current state immediately
    await websocket.send_json({"type": "init", "books": books})
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload["action"] == "add":
                new_book = {
                    "id": max(b["id"] for b in books) + 1 if books else 1,
                    "title": payload["title"],
                    "author": payload["author"]
                }
                books.append(new_book)
                await manager.broadcast({"type": "added", "book": new_book})
                
            elif payload["action"] == "delete":
                books[:] = [b for b in books if b["id"] != payload["id"]]
                await manager.broadcast({"type": "deleted", "id": payload["id"]})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)