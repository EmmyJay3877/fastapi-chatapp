from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
from users import add_users, remove_user, get_user, get_users_in_room
import json

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[],
    allow_headers=[],
)

socket_manager = SocketManager(app=app)

@app.get('/')
def root():
    return {"message": "Hello World, server up and running"}

@socket_manager.on('connect')
async def connect(sid, environ, *args):
    print(sid, 'connected')
    
    @socket_manager.on('join')
    async def join_room(sid, name: str, room: str, ):
        user = add_users(sid, name, room)

        if 'error' in user:
            return user['error']
            await socket_manager.disconnect(sid)
            
        socket_manager.enter_room(user['id'], user['room'])
        await socket_manager.emit('message', 
        {'user': 'admin', 'text': f"{user['name']}, Welcome to the {user['room']} room. Have Fun."}, 
        to=user['id'])
        await socket_manager.emit('message', 
        {'user': "admin", 'text': f"{user['name']} has joined."},
        room=user['room'], skip_sid=user['id'])
        await socket_manager.emit('roomdata', {'room': user['room'], 'users': get_users_in_room(user['room'])}, room=user['room'])

            
@socket_manager.on('send_msg')
async def send_message(sid, message):
    user = get_user(sid)
    await socket_manager.emit('message', {'user': user['name'], 'text': message}, room=user['room'])

@socket_manager.on('disconnect')
async def disconnect(sid):
    user = get_user(sid)
    if user:
        await socket_manager.emit('message', {'user': 'admin', 'text': f"{user['name']} left chat"}, room=user['room'])
        await socket_manager.emit('roomdata', {'room': user['room'], 'users': get_users_in_room(user['room'])}, room=user['room'])
    remove_user(sid)
    print(sid, 'disconnected')
