import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.db import Base, engine

import socketio
from socketio import ASGIApp
import uvicorn

fastapi_app = FastAPI(title="MetaSpace API")
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = ASGIApp(sio, other_asgi_app=fastapi_app)

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-mswzhfapn-ilkasus-projects.vercel.app",
    "https://meta-space-oo2t7fmki-ilkasus-projects.vercel.app"
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/")
def root():
    return {"message": "MetaSpace backend is running"}

fastapi_app.include_router(auth.router, prefix="/auth", tags=["Auth"])
fastapi_app.include_router(users.router, prefix="/users", tags=["Users"])

@sio.event
async def connect(sid, environ):
    print(f"🟢 Socket connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"🔴 Socket disconnected: {sid}")

@sio.event
async def send_message(sid, data):
    print(f"💬 New message from {sid}: {data}")
    await sio.emit("receive_message", data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
