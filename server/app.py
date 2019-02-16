import redis
import os, sys
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_socketio import SocketIO, send, emit
import time
from threading import Thread, Event
import eventlet
import json
from datetime import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'twitter_pipeline'))
from twitterStreaming import TwitterStreaming

eventlet.monkey_patch()
base_dir = os.path.abspath('../public')
app = Flask(__name__, template_folder=base_dir)
socketio = SocketIO(app)
ts_thread = None
s_thread = None

class sentimentValueStreaming(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        print('set up')
        self.p = self.r.pubsub()
        self.p.subscribe('sentimentData')
        self.event = Event()

    def run(self):
        print('start calculate value!!')
        time_format = '%a %b %d %H:%M:%S %z %Y'
        preTime = None
        curTime = None
        s_sum = 0
        s_count = 0
        while not self.event.is_set(): # <---- Added
            message = self.p.get_message()
            if message and isinstance(message['data'], bytes):
                sentimentData = json.loads(message['data'].decode('utf8'))
                curTime = datetime.strptime(sentimentData['created_at'], time_format)
                if preTime is None:
                    preTime = curTime
                    s_count += 1
                else:
                    if preTime.time() > curTime.time():
                        continue
                    elif preTime.time() == curTime.time():
                        s_sum += int(sentimentData['sentimentValue'])
                        s_count += 1
                    else:
                        sentimentValue = s_sum / s_count
                        created_at = str(curTime.hour).zfill(2) + ':' + \
                                     str(curTime.minute).zfill(2) + ':' + \
                                     str(curTime.second).zfill(2)
                        socketio.emit('message',
                              {'created_at': created_at, 'sentimentValue': sentimentValue},
                              namespace='/streaming_socket')
                        print(created_at + '   ' + str(sentimentValue))
                        s_sum = int(sentimentData['sentimentValue'])
                        s_count = 1
                        preTime = curTime

            socketio.sleep(0.00001)
    def stop(self):
        print('stop calculate value!!')
        self.event.set()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(base_dir, filename)

@app.route('/api/streaming/start', methods=['POST'])
def start_streaming():
    kws = []
    data = request.get_json()
    kws.append(data['query'])
    global ts_thread
    global s_thread
    if ts_thread is None and s_thread is None:
        print('start streaming!!')
        ts_thread = TwitterStreaming()
        s_thread = sentimentValueStreaming()
        ts_thread.start(keywords=kws)
        s_thread.start()
    else:
        print('stop first, then start streaming!!')
        ts_thread.stop()
        ts_thread.start(keywords=kws)

    return 'start streaming'

@app.route('/api/streaming/stop', methods=['POST'])
def stop_streaming():
    global ts_thread
    global s_thread

    print('stop streaming!!')
    if ts_thread is not None:
        ts_thread.stop()
    if s_thread is not None:
        s_thread.stop()

    return 'stop streaming'




if __name__ == '__main__':
    socketio.run(app, debug=True)
