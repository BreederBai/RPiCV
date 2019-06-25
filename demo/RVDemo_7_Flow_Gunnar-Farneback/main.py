# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import time
import cv2

def draw_flow(img, flow, step=10):
    tx=0
    ty=0
    t2x=0
    t2y=0
    numx=0
    numy =0
    tempXup=0 
    tempXdown=0
    tempYup=0 
    tempYdown =0
    flowX=0
    flowY=0
    maxX=0
    maxY=0
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T

    X = sorted(fx)
    Y = sorted(fy)
    for tx in X :
        if(tx>=0):
            tempXup = tempXup + tx
        elif(tx<0):
            tempXdown = tempXdown + tx
    if(tempXup >= tempXdown *-1 ):
        for t2x in X:
            if(t2x >= X[44]*0.6):
                flowX = flowX + t2x
                numx = numx +1
        flowX = int ( flowX / numx * 30 * 10 )  #30为hz数  10为保留1位小数
    if(tempXup < tempXdown *-1 ):
        for t2x in X:
            if(t2x <= X[3]*0.6):
                flowX = flowX + t2x
                numx = numx +1
        flowX = int( flowX / numx * 30 * 10 )

    for ty in Y :
        if(ty>=0):
            tempYup = tempYup + ty
        elif(ty<0):
            tempYdown = tempYdown + ty
    if(tempYup >= tempYdown *-1 ):
        for t2y in Y:
            if(t2y >= Y[44]*0.6):
                flowY = flowY + t2y
                numy = numy +1
        flowY = int( flowY / numy * 30 * 10 )
    if(tempYup < tempYdown *-1 ):
        for t2y in Y:
            if(t2y <= Y[3]*0.6):
                flowY = flowY + t2y
                numy = numy +1
        flowY = int( flowY / numy * 30 * 10 )


    print (flowX, flowY)
 

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 3)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 0, 255))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

#增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
cap = cv2.VideoCapture(0)
cap.set(3,80)#设置摄像头输出宽,
cap.set(4,60)#设置摄像头输出高,

time.sleep(2.0)


# Take first frame and find corners in it
ret, old_frame =  cap.read()
#old_frame=old_frame[70:170,110:210]
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
show_hsv = False
show_glitch = False
start_time = time.time()
fps_counter = 0
fps=0

while(1):
    ret, frame =  cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(old_gray, gray, None, 0.5, 3, 20, 3, 5, 1.1, 0)
    old_gray = gray
    gray_flow = draw_flow(gray, flow)

    fps_counter=fps_counter+1
    if (time.time() - start_time) > 1:
        fps=fps_counter / (time.time() - start_time)
        fps_counter = 0
        start_time = time.time()
        
    cv2.putText(gray_flow, "FPS : " + str( int( fps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
    cv2.imshow('flow',gray_flow)
    if cv2.waitKey(10) == 27:
        break
