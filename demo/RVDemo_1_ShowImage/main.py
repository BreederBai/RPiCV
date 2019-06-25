# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import cv2

frame = cv2.imread("sea.jpg")
frame = imutils.resize(frame, height=640,width=320)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

while(True):
    cv2.imshow('frame',frame)
    if cv2.waitKey(1000) == 27:
        break

    cv2.imshow('frame',gray)
    if cv2.waitKey(1000) == 27:
        break
