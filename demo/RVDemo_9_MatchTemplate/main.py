# -*- coding:utf-8 -*- 
import copy
import math
import numpy as np
import imutils
import cv2
import time

#获取被匹配图像--电路板图像
img_rgb = cv2.imread("1.jpg")
#将被匹配图像转换为灰度图像
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#获取匹配模板，LDO图像
template = cv2.imread("2.jpg",0)
#获取模板的高与宽
w, h = template.shape[::-1]
#执行模板匹配函数
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
#阈值设置为80%
threshold = 0.80
loc = np.where( res >= threshold)
cnt=0
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.putText(img_rgb, "LDO",(pt[0] + w, pt[1]),cv2.FONT_HERSHEY_SIMPLEX,2, (0,0,255), 1)
cv2.imshow('image',img_rgb)
cv2.waitKey(0)
 
