# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import cv2
import time
import os


#增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
cap = cv2.VideoCapture(0)
cap.set(3,320)#设置摄像头输出宽
cap.set(4,240)#设置摄像头输出高
print("start reading video...")
time.sleep(2.0)
print("start working")

t_start = time.time()
fps = 0

while True:
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转换灰色 
    # OpenCV人脸识别分类器 
    classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    color = (0, 255, 0) # 定义绘制颜色 
    # 调用识别人脸 
    faceRects = classifier.detectMultiScale( gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32)) 
    if len(faceRects): # 大于0则检测到人脸 
        for faceRect in faceRects: # 单独框出每一张人脸 
            x, y, w, h = faceRect 
            # 框出人脸 
            cv2.rectangle(img, (x, y), (x + h, y + w), color, 2) 
            # 左眼 
            cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8), color) 
            #右眼 
            cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8), color) 
            #嘴巴 
            cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4), (x + 5 * w // 8, y + 7 * h // 8), color)

    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(img, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

    cv2.imshow('img',img)
    if cv2.waitKey(10) == 27:
        break
