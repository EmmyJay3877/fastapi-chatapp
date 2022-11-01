users = []

def add_users(sid, name: str, room: str):
    name = name.lower()
    room = room.lower()
    existing_user = []
    for user in users:
        if user['name'] == name and user['room'] == room:
            existing_user.append(user)
    if not name and not room:
        return {'error': 'Username and Room is required'}
    if existing_user:
        return {'error': 'This username exists in the room'}

    new_user = {'id':sid, 'name':name, 'room':room}
    users.append(new_user)
    return new_user

def remove_user(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)

def get_user(id):
    for user in users:
        if user['id'] == id:
            return user

def get_users_in_room(room: str):
    users_in_a_room = []
    for user in users:
        if user['room'] == room:
            users_in_a_room.append(user)
    return users_in_a_room