from flask import session
from website import create_app
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import pickle
from website.models import User

app = create_app()
socketio = SocketIO(app)

def serialise_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'dateOfBirth': user.dateOfBirth.strftime('%Y-%m-%d'),
        'gender': user.gender
    }

@socketio.on('join')
def on_join(data):
    room = data
    join_room(room)
    user_json = session.get('user')
    if not user_json:
        user_json = session.get('doctor')
    user = pickle.loads(user_json)
    username = user.username
    send({'name': 'System', 'message': f'{username} has entered the room.'}, to=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    user_json = session.get('user')
    if not user_json:
        user_json = session.get('doctor')
    user = pickle.loads(user_json)
    username = user.username
    send({'name': 'System', 'message': f'{username} has left the room.'}, to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    user_json = session.get('user')
    if not user_json:
        user_json = session.get('doctor')
    user = pickle.loads(user_json)
    username = user.username
    content = {
        "name": username,
        "message": message
    }
    send(content, to=room)

@socketio.on('chat_request')
def handle_chat_request(data):
    room = data['room']
    userId = data['userId']
    user = User.query.filter_by(id=userId).first()
    user_json = serialise_user(user)
    message = data['message']
    content = {
        "room": room,
        "user_json": user_json,
        "message": message
    }
    emit('chat_request', content, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)