from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from helloworld import bloubiboulga

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('testlistenlive.html')

@socketio.on('output')
def handle_output(output):
    emit('output', output)

import sys

def redirect_output():
    for line in bloubiboulga():
        sys.stdout.write(line)
        sys.stdout.flush()
        socketio.emit('output', line)

if __name__ == '__main__':
    socketio.run(app)
