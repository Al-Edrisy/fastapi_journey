from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
import uuid

app = FastAPI(title="Real-Time Polling API")

class PollCreate(BaseModel):
    question: str
    options: List[str]

class PollResponse(BaseModel):
    id: str
    question: str
    options: List[str]
    votes: Dict[str, int]

# In-memory storage
polls: Dict[str, Dict] = {}

class ConnectionManager:
    def __init__(self):
        # poll_id -> list of active websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, poll_id: str):
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []
        self.active_connections[poll_id].append(websocket)

    def disconnect(self, websocket: WebSocket, poll_id: str):
        if poll_id in self.active_connections:
            if websocket in self.active_connections[poll_id]:
                self.active_connections[poll_id].remove(websocket)
            if not self.active_connections[poll_id]:
                del self.active_connections[poll_id]

    async def broadcast(self, poll_id: str, message: dict):
        if poll_id in self.active_connections:
            # We copy the list to avoid issues if a socket disconnects during broadcast
            for connection in list(self.active_connections[poll_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, poll_id)

manager = ConnectionManager()

@app.post("/polls", response_model=PollResponse)
async def create_poll(poll: PollCreate):
    poll_id = str(uuid.uuid4())
    new_poll = {
        "id": poll_id,
        "question": poll.question,
        "options": poll.options,
        "votes": {option: 0 for option in poll.options}
    }
    polls[poll_id] = new_poll
    return new_poll

@app.get("/polls", response_model=List[PollResponse])
async def list_polls():
    return list(polls.values())

@app.get("/polls/{poll_id}", response_model=PollResponse)
async def get_poll(poll_id: str):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    return polls[poll_id]

@app.post("/polls/{poll_id}/vote")
async def vote_rest(poll_id: str, option: str):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    if option not in polls[poll_id]["options"]:
        raise HTTPException(status_code=400, detail="Invalid option")
    
    polls[poll_id]["votes"][option] += 1
    
    # Broadcast to websocket clients
    await manager.broadcast(poll_id, polls[poll_id])
    
    return polls[poll_id]

@app.delete("/polls/{poll_id}")
async def delete_poll(poll_id: str):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    del polls[poll_id]
    return {"detail": "Poll deleted"}

@app.websocket("/ws/polls/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str):
    if poll_id not in polls:
        await websocket.close(code=4004)
        return

    await manager.connect(websocket, poll_id)
    # Send current state upon connection
    await websocket.send_json(polls[poll_id])
    
    try:
        while True:
            data = await websocket.receive_text()
            option = data.strip()
            if option in polls[poll_id]["options"]:
                polls[poll_id]["votes"][option] += 1
                # Broadcast updated poll
                await manager.broadcast(poll_id, polls[poll_id])
            else:
                await websocket.send_json({"error": "Invalid option"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, poll_id)

@app.get("/")
async def get():
    with open("app/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
