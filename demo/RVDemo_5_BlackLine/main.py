# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import serial
import time
import cv2
import math

# Black
Lower = np.array([0, 0, 0])
Upper = np.array([180, 255, 55])

#Position
Postion_x = 80
Postion_y = 60
angle =0 


#增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
cap = cv2.VideoCapture(0)
cap.set(3,320)#设置摄像头输出宽
cap.set(4,240)#设置摄像头输出高
print("start reading video...")
time.sleep(2.0)
print("start working")

t_start = time.time()
fps = 0

while(True):
    ret,frame = cap.read()
    frame = imutils.resize(frame, width=160)
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(HSV, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)

        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
        Postion_x = int( rect[0][0] )
        Postion_y = int( rect[0][1] )
        if (rect[0][0] > box[0][0]) :
            angle = int( - rect[2] )
        else :
            angle = int( -90 - rect[2])
    else :
        angle =0
        Postion_x = 80
        Postion_y = 60

    print(angle,Postion_y)
    
    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(frame, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

    cv2.imshow('frame',frame)

    if cv2.waitKey(10) == 27:
        break
