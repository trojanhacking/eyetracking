import cv2 #for display
import mediapipe as mp #for intelligence
import math


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


totalCountOfCloseness = 0
totalCountOfNot = 0

def depthTracking(landmarks):
    global totalCountOfCloseness, totalCountOfNot
    how_close = (round(landmarks.landmark[1].z * 1000))
    if (how_close < -80) :
        totalCountOfCloseness += 1
        totalCountOfNot = 0
        if (totalCountOfCloseness == 150):
            print("Too close")
        if (totalCountOfCloseness == 1):
            print("In range")
    else:
        if (totalCountOfNot > 50):
            totalCountOfCloseness = 0
        totalCountOfNot += 1

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

                
                depthTracking(landmarks)

                

                
                

                
        cv2.imshow('Eye Tracker', frame)
        #quite program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
