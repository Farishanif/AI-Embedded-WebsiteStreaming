app.py
from flask import Flask, render_template, request
import eventlet
# import os
from cryptography.fernet import Fernet
# import threading
import socketio
import base64
# import datetime
# import psycopg2
import eventlet.wsgi
from waitress import serve

#setup url web
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/stream')
def stream():
	return render_template('stream.html')

@app.route('/about')
def about():
	return render_template('about.html')

#setup websocket
sio = socketio.Server(cors_allowed_origins="*")#async_mode=async_mode)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

dict1={}
i=0

@sio.event()
def pingpong(sid):
	print("//////////////////////////")
	sio.emit("send_data", room=sid)
	sio.sleep(0)

@sio.event
def connect(sid, data):	
	print("[INFO] Connect to the server")
	pingpong(sid)

@sio.event
def send(sid, data):
	
	# key = data['key']
	# f = Fernet(key)
	# data = f.decrypt(data['frame'])
	key = b'sPy0VTSyePWQTR7mDmOeJbk6JWS5LfGyO0OJ7uiJxE8='
	data = Fernet(key).decrypt(data)
	data = base64.encodebytes(data)
	data = data.decode("utf-8")
	# print(data)
	global i
	if sid not in dict1:
		i+=1
		dict1[sid]=i
	key=dict1[sid]
	print("Reached here")
	# db = threading.Thread(target=thread_db, args=(data,))
	# db.start()
	sio.emit('response',{'key':key, 'data':data})
	pingpong(sid)
	sio.sleep(20)

@sio.event
def disconnect(sid):
	print("[INFO] disconnected from the server")

if __name__ == '__main__':
	eventlet.wsgi.server(eventlet.listen(('',5000)), app)
	# serve(app, port=5000, host="192.168.43.46")
	
