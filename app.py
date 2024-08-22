from flask import session
from website import create_app
from flask_socketio import SocketIO, join_room, leave_room, send
import pickle

app = create_app()
socketio = SocketIO(app)

@socketio.on('join')
def on_join(data):
    room = data
    join_room(room)
    user_json = session.get('user')
    user = pickle.loads(user_json)
    username = user.username
    send({'name': 'System', 'message': f'{username} has entered the room.'}, to=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    user_json = session.get('user')
    user = pickle.loads(user_json)
    username = user.username
    send({'name': 'System', 'message': f'{username} has left the room.'}, to=room)

@socketio.on('message')
def handle_message(data):
    print(data.keys())
    # room = data.get('room')
    room = data['room']
    message = data['message']
    user_json = session.get('user')
    user = pickle.loads(user_json)    
    username = user.username
    content = {
        "name": username,
        "message": message
    }
    send(content, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)