import cv2
import time
import posemodule as pm

cap = cv2.VideoCapture("Resources/me_walking.mp4")
cap.set(3,1080)
cap.set(4,720)
cap.set(10,100)
past = 0
detector = pm.poseDetector()
while True:
    success, img = cap.read()
    img = cv2.resize(img,(600,650))
    img = detector.findPose(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
            print(lmlist[14])
            cv2.circle(img,(lmlist[14][1],lmlist[14][2]),15,(0,0,255),cv2.FILLED)
    
    current = time.time()
    fps=1/(current-past)
    past = current
    
    cv2.putText(img,str(int(fps)),(0,500),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),4)
    cv2.imshow("video",img)
    if cv2.waitKey(1) &0xFF == ord('e'):
        break