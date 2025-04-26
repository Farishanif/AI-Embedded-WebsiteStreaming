client.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
from telebot import *
import socketio
import cv2
import json
import base64
import yolo
from time import sleep
cap=cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
sio = socketio.Client(engineio_logger=True)
i=0;
api = '5484531444:AAHjI5X1W4zJ4QQm_3ruG-QPk0X6Kk-dH44'
bot = telebot.TeleBot(api)
receive_id = 1416579323

@sio.event
def connect():
    print("CONNECTED")

@sio.event
def send_data():
    while(cap.isOpened()):
        key = b'sPy0VTSyePWQTR7mDmOeJbk6JWS5LfGyO0OJ7uiJxE8='
        ret,img=cap.read()
        if ret:
            #img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            img = cv2.flip(img, 0)
            #get fungsi yolo
            data = yolo.detect(img)
            #return image
            frame = data[0]
            indexes = data[1]
            print(indexes)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame = base64.encodebytes(frame)
            frame = Fernet(key).encrypt(frame)
            frame = frame.decode("utf-8")
            message(frame)
            sleep(0)
            
            key = cv2.waitKey(1)
    
            if key == 27:
                break 
            if key == ord('i'):
                cv2.imwrite('image.jpg',img)
            if key == ord('i'):
                cv2.imwrite(f'detect_{i}.jpg',img)
                i+=1
            if len(indexes)>0:
                detected = f'Kedetect_{i}.jpg'
                cv2.imwrite(detected,img)
                i+=1
                #chatid = message.chat.id
                bot.send_photo(receive_id, open(detected, 'rb'))

            bot.polling()
            #cap.release()
        else:
            break

def message(json):
    print("/////////////////////////////500")
    #sio.emit('send',str(i))
    sio.emit('send', json)

@sio.event
def disconnect():
    print("DISCONNECTED")

if __name__ == '__main__':
    sio.connect('http://192.168.43.46:5000') ##43.46 uncomment this line when the server is on remote system change the ip address with the ip address 
    #of the system where the server is running.
    #sio.connect('0.0.0.0:5000')
    sio.wait()
