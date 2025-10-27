import cv2 #for display
import mediapipe as mp #for intelligence
import math
from datetime import datetime



mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
start_time = datetime.now()
blinked = False
nonBlinkedTimer = 0
shownBlink = False

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, fr = cap.read()
        frame = cv2.flip(fr, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w, _ = frame.shape

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks: #primary face
                h, w, _ = frame.shape

                for id, lm in enumerate(landmarks.landmark):
                
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (x, y), 1, (0,255,0), -1)
                
                cv2.circle(frame, (int(landmarks.landmark[159].x * w), int(landmarks.landmark[159].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
                cv2.circle(frame, (int(landmarks.landmark[145].x * w), int(landmarks.landmark[145].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
                leftEyeBlink = abs(landmarks.landmark[159].y * h - landmarks.landmark[145].y * h)
                if leftEyeBlink < 4:
                    blinked = True
                    start_time = datetime.now()
                    blinked = False
                    shownBlink = False
                
                
                
                if blinked == False:
                    nonBlinkedTimer = datetime.now() - start_time
                    if nonBlinkedTimer.total_seconds() >= 7:
                        if shownBlink == False:
                            print("BLINK NOW DUDE")
                            shownBlink = True
                            
                    

      
        cv2.imshow('Eye Tracker', frame)
        #quit program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
