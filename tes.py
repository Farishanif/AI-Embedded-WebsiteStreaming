import cv2
import numpy as np
import os
from time import sleep
import base64
from cryptography.fernet import Fernet
from telebot import *

#manggil hasil training data
net = cv2.dnn.readNet('yolov4-tiny-custom_best.weights', 'yolov4-tiny-custom.cfg')

classes = []
with open("obj.names", "r") as f:
    classes = f.read().splitlines()

#declare untuk save video agar bisa append
i=0

#declare height, width 
h , w =  None, None

#set untuk save video hasil live
writer = None

#set parameter untuk source
cap = cv2.VideoCapture(0)
#img = cv2.imread('brownspot.jpg')

#telegram key 
api = '5484531444:AAHjI5X1W4zJ4QQm_3ruG-QPk0X6Kk-dH44'
bot = telebot.TeleBot(api)
receive_id = 1416579323

layerOutputs = []

start_time=time.time()

_, img = cap.read()

def trainingBackground():

    while True:
        #check jika source nya bernilai true 
        global _, img
        _, img = cap.read()

        #declare untuk mengambil inference time dan fps
        global start_time
        start_time=time.time()
        height, width ,_ =img.shape
        global w, h     
        # Getting dimensions of the frame for once as everytime dimensions will be same      
        if w is None or h is None:
            # Slicing and get height, width of the image
            h, w = img.shape[:2]

        #set agar input size sesuai dengan hasil training
        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        global layerOutputs
        layerOutputs = net.forward(output_layers_names)

def displayVideo():
    


    while True:
        #mulai membuat bounding box
        boxes = []
        confidences = []
        class_ids = []
        if layerOutputs:
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.2:
                        box_current = detection[0:4] * np.array([w, h, w, h])

                        x_center, y_center, box_width, box_height = box_current
                        x_min = int(x_center - (box_width / 2))
                        y_min = int(y_center - (box_height / 2))

                        boxes.append([x_min, y_min, int(box_width), int(box_height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        #boxes.append([x, y, w, h])
                        #confidences.append((float(confidence)))
                        #class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))

            if len(indexes)>0:
                for i in indexes.flatten():
                    #x, y, w, h = boxes[i]
                    x_min, y_min = boxes[i][0], boxes[i][1]
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i],2))
                    color = colors[i]
                    cv2.rectangle(img, [x_min, y_min, int(box_width), int(box_height)], color, 2)
                    cv2.putText(img, label + " " + confidence, (x_min, y_min+20), font, 2, (255,255,255), 2)
            
            #menampilkan inference dan fps time 
            curent_time=time.time()
            if curent_time > start_time:              
                inference_time=curent_time-start_time
                fps=1/inference_time
                print("inference time:" , inference_time)
                fps = int(fps)
                fps = str(fps)
                print("fps:" , fps)
                cv2.putText(img, fps, (7, 70), font, 3, (200, 255, 0), 3, cv2.LINE_AA) 
                cv2.imshow('Image', img)          
                key = cv2.waitKey(1)

                global writer 
                # Initialize writer (save hasil live berupa video)
                if writer is None:
                    resultVideo = cv2.VideoWriter_fourcc(*'mp4v')

                    # Writing current processed frame into the video file
                    writer = cv2.VideoWriter('result-video.mp4', resultVideo, 30,
                                            (img.shape[1], img.shape[0]), True)

                # Write processed current frame to the file
                writer.write(img)

                #key input untuk exit dan save gambar 
                if key == 27:
                    return False 
                if key == ord('i'):
                    cv2.imwrite(f'detect_{i}.jpg',img)
                    i+=1
                if len(indexes)>0:
                    detected = f'Kedetect_{i}.jpg'
                    cv2.imwrite(detected,img)
                    i+=1
                    #chatid = message.chat.id
                    bot.send_photo(receive_id, open(detected, 'rb'))

    writer.release()
    bot.polling()
    cap.release()
    cv2.destroyAllWindows


if __name__ == '__main__':
    c = threading.Thread(name='trainingBackground', target=trainingBackground)
    c.daemon = True
    c.start()
    displayVideo()