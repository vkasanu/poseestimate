#***************************************************************
#Version 1: Outlook of Gait Analysis                           *
#Note: tracking only one side at a time is not feasible        *
#Aim : To reduce the code size to satisfy memory constraints   *
#Frame size: 900 * 600                                         *
#Laser lines: 10% from both edges (right and left) |           *
#             20% from bottom of the frame                     *
# Gait Analysis Range: 3 meters                                *
#***************************************************************
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture("Resources/me_walking.mp4") 

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (900, 600))

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        results = pose.process(frame_rgb)

  
        if results.pose_landmarks:
       
            left_side_landmarks = [
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
            ]
            
            right_side_landmarks = [
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE],
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
            ]

        
            for landmark in left_side_landmarks:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 165, 255), -1)  

   
            for connection in [(0, 1), (1, 2), (2, 3)]:
                pt1 = (int(left_side_landmarks[connection[0]].x * frame.shape[1]),
                       int(left_side_landmarks[connection[0]].y * frame.shape[0]))
                pt2 = (int(left_side_landmarks[connection[1]].x * frame.shape[1]),
                       int(left_side_landmarks[connection[1]].y * frame.shape[0]))
                cv2.line(frame, pt1, pt2, (203, 192, 255), 2) 

  
            for landmark in right_side_landmarks:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 165, 255), -1)  

          
            for connection in [(0, 1), (1, 2), (2, 3)]:
                pt1 = (int(right_side_landmarks[connection[0]].x * frame.shape[1]),
                       int(right_side_landmarks[connection[0]].y * frame.shape[0]))
                pt2 = (int(right_side_landmarks[connection[1]].x * frame.shape[1]),
                       int(right_side_landmarks[connection[1]].y * frame.shape[0]))
                cv2.line(frame, pt1, pt2, (203, 192, 255), 2)  
        
    
        vertical_line_x1 = int(frame.shape[1] * 0.10)  # 25% from the left
        vertical_line_x2 = int(frame.shape[1] * 0.90)  # 75% from the left
        cv2.line(frame, (vertical_line_x1, 0), (vertical_line_x1, frame.shape[0]), (0, 0, 255), 2)  # Blue color
        cv2.line(frame, (vertical_line_x2, 0), (vertical_line_x2, frame.shape[0]), (0, 0, 255), 2)  # Blue color
        
      
        horizontal_line_y = frame.shape[0] - int(frame.shape[0] * 0.20)  # 25% from the bottom
        cv2.line(frame, (0, horizontal_line_y), (frame.shape[1], horizontal_line_y), (0, 0, 255), 2)  # Blue color

       
        cv2.imshow('Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
