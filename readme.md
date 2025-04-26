# AI Embedded Website Streaming

.VENV <br>
.venv is a simple Flask website that can connect into Websocket client on any device with compatible module Socket.io library, used for receiving a live video stream equipped with fernet encrypted reader for each live video stream transmission while also sending each rice disease detected frame into postgreSQL database.

Client.py <br>
Client.py is a python program that is created to send a livestream feed into Flask website.venv, connected with yolo.py the main AI program. Same with .venv Client.py equipped with Socket.io and fernet encryipter. This program mainly controlling the sending of a live video stream into the socket.io receiver which is .venv.

Yolo.py <br>
Yolo.py is the main ai program which containing a fast and light performance CNN (YoloV4) weight and model that has been trained on rice disease dataset. This program will detect the rice disease part of each live video frame and will mark and border it with the help of OpenCV library, while also give a message into WhatsApp application if detected the rice disease via Telebot library.

