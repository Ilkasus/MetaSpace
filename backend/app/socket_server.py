import asyncio
import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

connected_users = set()

@sio.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')
    connected_users.add(sid)
    await sio.emit('users_count', len(connected_users))

@sio.event
async def disconnect(sid):
    print(f'Client disconnected: {sid}')
    connected_users.discard(sid)
    await sio.emit('users_count', len(connected_users))

@sio.event
async def message(sid, data):
    print(f'Message from {sid}: {data}')
    await sio.emit('message', data)  # ретранслируем всем

if __name__ == '__main__':
    web.run_app(app, port=5000)
