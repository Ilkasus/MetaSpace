import os
import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-git-main-ilkasus-projects.vercel.app",
    "https://meta-space-en8fzv3kn-ilkasus-projects.vercel.app"
]

fastapi_app = FastAPI(title="MetaSpace API")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(auth.router, prefix="/auth", tags=["Auth"])
fastapi_app.include_router(users.router, prefix="/users", tags=["Users"])

@fastapi_app.get("/")
async def root():
    return {"message": "MetaSpace backend is running"}

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins
)

connected_players = {}

@sio.event
async def connect(sid, environ, auth):
    print(f"🔌 Client connected: {sid}")
    connected_players[sid] = {
        "nickname": None,
        "position": [0, 0, 0],
        "rotation": [0, 0, 0]
    }
    await sio.emit("players_update", connected_players)
    await sio.emit("users_count", len(connected_players))

@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")
    connected_players.pop(sid, None)
    await sio.emit("players_update", connected_players)
    await sio.emit("users_count", len(connected_players))

@sio.event
async def chat_message(sid, data):
    nickname = data.get("nickname", "Anonymous")
    text = data.get("text", "")
    print(f"💬 {nickname}: {text}")
    await sio.emit("receive_message", {"nickname": nickname, "text": text})

@sio.event
async def player_move(sid, data):
    if sid in connected_players:
        connected_players[sid].update(data)
    await sio.emit("players_update", connected_players, skip_sid=sid)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
