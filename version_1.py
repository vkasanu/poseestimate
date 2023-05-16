#version1
import cv2
import mediapipe as mp
import time
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose=mpPose.Pose()
cap=cv2.VideoCapture("Resources/me_walking.mp4")
past=0
while  True:
    Success, img = cap.read()
    img = cv2.resize(img,(640,480))
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id,lm)
            cx,cy = int(lm.x*w),int(lm.y*h)
    cur = time.time()
    fps = 1/(cur-past)
    past = cur
    cv2.putText(img,str("Frames per second = "),(20,430),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    cv2.putText(img,str(int(fps)),(220,430),cv2.FONT_HERSHEY_PLAIN,1,(0,165,255),2)
    cv2.imshow("video",img)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break


