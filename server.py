from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG'] = False
socketio = SocketIO(app)

@app.route('/')
def index():
    return "hello world"

@socketio.on("message form user", namespace='/messages')   
def receive_message_from_user(message):
    print(request.sid)
    print('user message {}'. format(message)) 

@socketio.on('username', namespace='/private')
def receive_username(username):  
    users[username] = request.sid
    print(users)

@socketio.on("private_message", namespace='/private')
def private_message(paylaod):

    print(paylaod)
    recipient_session_id = users[paylaod['username']]

    print(recipient_session_id)
    message = paylaod['message']
    emit('new_private_message', message, room=recipient_session_id)




# run forever
if __name__ == '__main__':
	socketio.run(app.run(host='0.0.0.0'))    