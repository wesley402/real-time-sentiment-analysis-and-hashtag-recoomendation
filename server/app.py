import redis
import os, sys
from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import time
from threading import Thread
import eventlet
eventlet.monkey_patch()
base_dir = os.path.abspath('../public')
app = Flask(__name__, template_folder=base_dir)
socketio = SocketIO(app)
thread = None

def background():
    count = 0
    while True:
        socketio.sleep(1)
        print(count)
        count = count + 1
        socketio.emit('message', {'data': count}, namespace='/streaming_socket')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(base_dir, filename)

@app.route('/api/stream', methods=['GET'])
def streaming():
    print('start!!!!!!!!!!!!streaming!!!!!!!!!')
    global thread
    if thread is None:
        thread = Thread(target=background)
        thread.start()
    return 'start streaming'


if __name__ == '__main__':
    socketio.run(app, debug=True)
