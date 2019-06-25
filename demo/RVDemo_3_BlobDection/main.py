# -*- coding:utf-8 -*- 
import numpy as np
import imutils
import time
import cv2


t_start = time.time()
fps = 0

if __name__ == '__main__':

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 20
    params.maxThreshold = 200

    # Filter by Color.
    params.filterByColor = True
    params.blobColor = 0

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else :
        detector = cv2.SimpleBlobDetector_create(params)

    #增加了底层驱动，可以直接通过cv2的0号设备读取摄像头
    cap = cv2.VideoCapture(0)
    cap.set(3,320)#设置摄像头输出宽
    cap.set(4,240)#设置摄像头输出高
    print("start reading video...")
    time.sleep(2.0)
    print("start working")

    while(True):
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=320)
        keypoints = detector.detect(frame)
        if(keypoints):
            for i in range (0, len(keypoints)):
                x = keypoints[i].pt[0]
                y = keypoints[i].pt[1]
                Postion_x = int(x*100)
                Postion_y = int(y*100)
        else:
            Postion_x = 8000
            Postion_y = 6000
        
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,255,255),cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

        # Calculate and show the FPS
        fps = fps + 1
        sfps = fps / (time.time() - t_start)
        cv2.putText(im_with_keypoints, "FPS : " + str( int( sfps ) ), ( 10, 15 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

        cv2.imshow("frame",im_with_keypoints)
        
        if cv2.waitKey(10) == 27:
            break

        print(Postion_x,Postion_y)
