import cv2
import numpy as np
import time
import posemodule as pm


detector = pm.poseDetector()
cap = cv2.VideoCapture("Resources/workout3.mp4")
count =0
dir=0
while True:
    success,img = cap.read()
    #img = cv2.imread("Resources/plank.jpg")
    #qimg = cv2.resize(img,(1080,720))

    
    img = detector.findPose(img,draw=True)
    lmlist = detector.findPosition(img,draw=True)
    if len(lmlist)!=0:
        angle = detector.findAngle(img,11,13,15)
        per = np.interp(angle,(187,270),(0,100))
        #print(angle,per)

        if per == 100:
            if dir ==0:
                count +=0.5
                dir=1
        if per == 0:
            if dir==1:
                count +=0.5
                dir=0
        print(count)


    cv2.imshow("image",img)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
