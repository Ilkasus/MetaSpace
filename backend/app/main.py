import os
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.db import Base, engine
import uvicorn

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-mswzhfapn-ilkasus-projects.vercel.app",
    "https://meta-space-oo2t7fmki-ilkasus-projects.vercel.app"
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
    async_mode='asgi',
    cors_allowed_origins=origins
)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def chat_message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit('receive_message', data)

@sio.event
async def player_move(sid, data):
    await sio.emit('players_update', data, skip_sid=sid)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

