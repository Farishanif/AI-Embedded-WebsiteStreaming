from flask import Flask, render_template, request
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import socketio
import os
import cv2
import json
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from time import sleep
cap=cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   
sio = socketio.Client(engineio_logger=True)
i=0;

@sio.event
def connect():
    print("CONNECTED")

@sio.event
def send_data():
    while(cap.isOpened()):
        key = b'sPy0VTSyePWQTR7mDmOeJbk6JWS5LfGyO0OJ7uiJxE8='
#         password = b"test" 
#         salt = os.urandom(16)
#         kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
#                  length=32,
#                  salt=salt,
#                  iterations=100000,
#                  )
#         key = base64.urlsafe_b64encode(kdf.derive(password)) 
#         f = Fernet(key)
        ret,img=cap.read()
        if ret:
#             img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            img = cv2.flip(img, 0)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
#             frame = base64.encodebytes(frame)
#             frame = f.encrypt(frame)
            frame = Fernet(key).encrypt(frame)
#             frame = frame.decode("utf-8")
#             data = json.dumps({'frame': frame, 'key': key })
            message(frame)
            sleep(20)
        else:
            break

def message(json):
    print("/////////////////////////////500")
    #sio.emit('send',str(i))
    sio.emit('send', json)

@sio.event
def reconnect():
    sio.reconnect()

@sio.event
def disconnect():
    print("DISCONNECTED")

if __name__ == '__main__':
    sio.connect('http://192.168.1.13:5000') ##43.46 uncomment this line when the server is on remote system change the ip address with the ip address 
    #of the system where the server is running.
    #sio.connect('0.0.0.0:5000')
    sio.wait()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        client_socket.close()
