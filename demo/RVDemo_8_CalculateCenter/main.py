# -*- coding:utf-8 -*- 
# import the necessary packages
import argparse
import imutils
import cv2

#读取demo.png
image = cv2.imread("demo.png")
#转为gray灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#5×5 内核的高斯平滑
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#阈值化
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

#该函数返回图像上每一个白块对应的边界点集合（即轮廓）
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print cnts
# loop over the contours
for c in cnts:
    #计算轮廓区域图像的矩
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
 
    # 调用 cv2.drawContours 函数绘制包围当前形状的轮廓
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    #在形状的中心 (cX, cY) 处绘制一个白色的小圆；
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    #在白色小圆的附近写上文字 center。
    cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #输出图像
    cv2.imshow('image',image)
    if cv2.waitKey(10) == 27:
        break

cv2.waitKey(0)
