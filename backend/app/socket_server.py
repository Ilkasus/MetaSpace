import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins=[
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-mswzhfapn-ilkasus-projects.vercel.app",
    "https://meta-space-oo2t7fmki-ilkasus-projects.vercel.app"
])
app = web.Application()
sio.attach(app)

connected_players = {}

@sio.event
async def connect(sid, environ):
    print(f"🔌 Client connected: {sid}")
    connected_players[sid] = {
        "nickname": None,
        "position": [0, 0, 0],
        "rotation": [0, 0, 0]
    }
    await sio.emit('players_update', connected_players)
    await sio.emit('users_count', len(connected_players))

@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")
    connected_players.pop(sid, None)
    await sio.emit('players_update', connected_players)
    await sio.emit('users_count', len(connected_players))

@sio.event
async def chat_message(sid, data):
    nickname = data.get('nickname', 'Anonymous')
    text = data.get('text', '')
    print(f"💬 chat_message received from {sid}: {nickname}: {text}")
    await sio.emit('receive_message', {'nickname': nickname, 'text': text})

@sio.event
async def player_move(sid, data):
    if sid in connected_players:
        connected_players[sid].update(data)
    await sio.emit('players_update', connected_players)

socket_app = app
