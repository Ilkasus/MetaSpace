import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = socketio.ASGIApp(sio, other_asgi_app=app)

@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")

@sio.event
async def send_comment(sid, data):
    print(f"Comment received: {data}")
    await sio.emit('new_comment', data)

@sio.event
async def disconnect(sid):
    print(f"User disconnected: {sid}")
