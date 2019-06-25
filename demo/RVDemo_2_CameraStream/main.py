# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import cv2
import time


cap = cv2.VideoCapture(0)
cap.set(3,320)#设置摄像头输出宽
cap.set(4,240)#设置摄像头输出高

print("start reading video...")
time.sleep(1.0)
print("start working")

t_start = time.time()
fps = 0

while(True):
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgAdapt = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    
    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(frame, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

    cv2.imshow('frame',frame)

    if cv2.waitKey(10) == 27:
        break
