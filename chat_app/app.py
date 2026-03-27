from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatapp_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Online users tracker
online_users = {}

COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
    '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
    '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA'
]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('join')
def handle_join(data):
    username = data.get('username', 'Anonymous')
    room = data.get('room', 'general')
    color = random.choice(COLORS)
    
    join_room(room)
    online_users[request.sid] = {
        'username': username,
        'room': room,
        'color': color,
        'joined_at': datetime.now().strftime('%H:%M')
    }
    
    emit('user_joined', {
        'username': username,
        'color': color,
        'time': datetime.now().strftime('%H:%M'),
        'online_count': len([u for u in online_users.values() if u['room'] == room])
    }, to=room)
    
    emit('user_list', {
        'users': [
            {'username': u['username'], 'color': u['color']}
            for u in online_users.values() if u['room'] == room
        ]
    }, to=room)

@socketio.on('message')
def handle_message(data):
    user = online_users.get(request.sid)
    if not user:
        return
    
    emit('message', {
        'username': user['username'],
        'color': user['color'],
        'text': data.get('text', ''),
        'time': datetime.now().strftime('%H:%M'),
        'sid': request.sid
    }, to=user['room'])

@socketio.on('typing')
def handle_typing(data):
    user = online_users.get(request.sid)
    if user:
        emit('typing', {
            'username': user['username'],
            'is_typing': data.get('is_typing', False)
        }, to=user['room'], include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    user = online_users.pop(request.sid, None)
    if user:
        emit('user_left', {
            'username': user['username'],
            'time': datetime.now().strftime('%H:%M'),
            'online_count': len([u for u in online_users.values() if u['room'] == user['room']])
        }, to=user['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
