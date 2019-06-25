# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import time
import cv2


#OpticalFlow
OpticalFlow_x = 0
OpticalFlow_y = 0
LastOpticalFlow_x = 0
LastOpticalFlow_y = 0
Shitomasi_x = 0
Shitomasi_y = 0
OpticalFlow_cnt = 0
OpticalFlow_flag = 0
a = 0
b = 0
c = 0
d = 0

#增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
cap = cv2.VideoCapture(0)
cap.set(3,320)#设置摄像头输出宽
cap.set(4,240)#设置摄像头输出高
print("start reading video...")
time.sleep(2.0)
print("start working")

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 5,
                       qualityLevel = 0.3,
                       minDistance = 1,
                       blockSize = 1 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (5,5),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_frame = imutils.resize(old_frame, width=160)
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
start_time = time.time()
fps_counter = 0
fps=0
conersCnt=0
speed=[0,0]
while(1):
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=160)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    if(p1 is None):
        old_gray = frame_gray.copy()
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        if(p0 is None):
            print("p0 is None")
        mask = np.zeros_like(old_frame)
	OpticalFlow_flag = 0
    else:
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        # draw the tracks
        conersCnt = len(good_new)
        speedx=np.zeros(conersCnt)
        speedy=np.zeros(conersCnt)
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            speedx[i]= (a-c) * 30
            speedy[i]= (b-d) * 30
            mask = cv2.line(mask, (a,b),(c,d), color[i+1].tolist(), 1)
            frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        old_gray = frame_gray.copy()
        speed=[np.mean(speedx),np.mean(speedy)]
        p0 = good_new.reshape(-1,1,2)
    img = cv2.add(frame,mask)
    cv2.imshow('img',img)
    if conersCnt > 0 :
        #数据保留小数点后一位
        x= int(speed[0] * 10)
        y= int(speed[1] * 10)
        print ("speedX: %.1f ,speedY: %.1f"%(x,y))
    else:
        print "None coners"
    fps_counter=fps_counter+1
    if (time.time() - start_time) > 1:
        fps=fps_counter / (time.time() - start_time)
        print("FPS: %.1f"%(fps))
        fps_counter = 0
        start_time = time.time()
