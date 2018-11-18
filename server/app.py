import redis
import os, sys
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_socketio import SocketIO, send, emit
import time
from threading import Thread
import eventlet
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'twitter_pipeline'))
from twitterStreaming import TwitterStreaming

eventlet.monkey_patch()
base_dir = os.path.abspath('../public')
app = Flask(__name__, template_folder=base_dir)
socketio = SocketIO(app)
ts_thread = None

def background():

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        sentimentValue = r.get('sentimentValue').decode('UTF-8')
        created_at = r.get('created_at').decode('UTF-8')
        print(sentimentValue)
        print(created_at)
        socketio.emit('message',
                      {'sentimentValue': sentimentValue, 'created_at': created_at}, namespace='/streaming_socket')
        socketio.sleep(0.05)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(base_dir, filename)

@app.route('/api/streaming/start', methods=['POST'])
def start_streaming():
    kws = 'taiwan'
    global ts_thread
    if ts_thread is None:
        print('start streaming!!')
        ts_thread = TwitterStreaming()
        ts_thread.start(keywords=kws)
    else:
        print('stop first, then start streaming!!')
        ts_thread.stop()
        ts_thread.start(keywords=kws)

    return 'start streaming'

@app.route('/api/streaming/stop', methods=['POST'])
def stop_streaming():
    global ts_thread
    print('stop streaming!!')
    if ts_thread is not None:
        ts_thread.stop()

    return 'stop streaming'




if __name__ == '__main__':
    socketio.run(app, debug=True)
