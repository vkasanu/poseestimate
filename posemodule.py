import cv2
import time
import mediapipe as mp
import math


class poseDetector():
    def __init__(self, mode=False, upperbody = False, smootheness = True, detectioncon=0.5,trackcon= 0.5):
        self.mode = mode
        self.upbody = upperbody
        self.smooth = smootheness
        self.detcon = detectioncon
        self.trackcon= trackcon
        self.mpDraw= mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self,img,draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                print(lm)
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw :
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
        return self.lmlist
    

    def findAngle(self,img,p1,p2,p3,draw = True):
        x1,y1=self.lmlist[p1][1:]
        x2,y2=self.lmlist[p2][1:]
        x3,y3=self.lmlist[p3][1:]

        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle < 0:
            angle +=360
        #print(angle) 

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),5)
            cv2.line(img,(x2,y2),(x3,y3),(255,255,255),5)
            cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
            cv2.circle(img,(x3,y3),10,(255,0,0),cv2.FILLED)


def main():
    cap = cv2.VideoCapture(0)
    past = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(600,650))
        img = detector.findPose(img,draw=True)

        #lmlist = detector.findPosition(img,draw=True)
        #if len(lmlist)!=0:
        #    print(lmlist)
            #cv2.circle(img,(lmlist[14][1],lmlist[14][2]),15,(0,0,255),3,cv2.FILLED)
        current = time.time()
        fps=1/(current-past)
        past = current
      #  cv2.ellipse(img,(234,24),(3,3),0,0,180,(0,0,255))
        cv2.putText(img,str(int(fps)),(0,500),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),4)
        #cv2.imshow("video",img)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    
if __name__=="__main__":
    main()