# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import time
import cv2
import multiprocessing



#计算全局光流值
def calFlow(img,flow,step=10):
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
    return flowX,flowY

#计算光流进程---占一个核
def Flow(frameQueue,firstFrame,flowX,flowY):
    old_frame = imutils.resize(firstFrame, width=80,height=60)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    while(True):
        if not frameQueue.empty():
            frame = frameQueue.get()
            frame = imutils.resize(frame, width=80,height=60)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # calculate optical flow
            # flow = cv2.calcOpticalFlowFarneback(old_gray, gray, 0.5, 3, 15, 3, 5, 1.1,0)
            flow = cv2.calcOpticalFlowFarneback(old_gray, gray, None, 0.5, 3, 20, 3, 5, 1.1, 0)
            old_gray = gray
            xSpeed,ySpeed=calFlow(gray,flow) 
            try:
                flowX.put(xSpeed,False)
                flowY.put(ySpeed,False)
            except:
                continue




if __name__ == '__main__':
    #增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
    cap = cv2.VideoCapture(0)
    cap.set(3,320)#设置摄像头输出宽
    cap.set(4,240)#设置摄像头输出高
    print("start reading video...")
    time.sleep(2.0)
    print("start working")
    #取一帧首图---为了后面光流的启动
    ret,firstFrame = cap.read()
    #创建主进程与光流进程之间的共享变量
    flowX=multiprocessing.Queue(maxsize=1)
    flowY=multiprocessing.Queue(maxsize=1)
    #创建图像队列
    frameQueue = multiprocessing.Queue(maxsize=1)
    #创建光流进程
    processFlow = multiprocessing.Process(target=Flow, args=(frameQueue,firstFrame,flowX,flowY))
    #运行光流进程
    processFlow.start()
    #初始化主线程中的光流变量
    xSpeed=0
    ySpeed=0
    #初始化主线程中的寻线变量
    # Black
    Lower = np.array([0, 0, 0])
    Upper = np.array([180, 255, 55])
    #Position
    Postion_x = 80
    Postion_y = 60
    angle =0
    t_start = time.time()
    fps = 0
    while(True):
#```````````````````获取图像``````````````````````
        ret,frame = cap.read()
#```````````````````向光流进程送入图像````````````
        try:
            frameQueue.put(frame,False)
        except:
            continue
#```````````````````处理寻线程序``````````````````
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
#```````````````````接收光流计算结果``````````````
        if not flowX.empty():
            xSpeed=flowX.get()
            ySpeed=flowY.get()
        print ("xSpeed: %d ,ySpeed: %d"%(xSpeed,ySpeed))

        # Calculate and show the FPS
        fps = fps + 1
        sfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

        cv2.imshow('frame',frame)
        if cv2.waitKey(10) == 27:
            break
