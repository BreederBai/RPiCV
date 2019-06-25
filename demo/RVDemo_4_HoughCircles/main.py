# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import time
import cv2


# Circle center
Circle_x = 0
Circle_y = 0
Circle_cnt = 0

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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=30,minRadius=0,maxRadius=0)
    if circles is not None:
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(gray,(i[0],i[1]),i[2],(255,0,0),2)
            # draw the center of the circle
            cv2.circle(gray,(i[0],i[1]),2,(255,0,0),3)
            Circles_x = int(i[0] * 100)
            Circles_y = int(i[1] * 100)
    else:
        Circles_x = 8000
        Circles_y = 6000
        print("Circles X:",Circles_x,"Circles Y:",Circles_y)

    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(gray, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

    cv2.imshow('gray',gray)

    if cv2.waitKey(10) == 27:
        break
