import cv2 #for display
import mediapipe as mp #for intelligence
from utility import *
import numpy as np
from eyeAngle import *
from constants import *
import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()
lastFalse = -1
lastTrue = -1
bg = time.time()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


# def circ_tripoint_to_vector(left, mid, right):
#     backMid = right - left
#     forward = mid - backMid
#     return forward / np.linalg.norm(forward)

# def calculate_look_vector(landmarks, w, h):
#     leftVector = circ_tripoint_to_vector(
#         normalizedLandmark_to_numpyVector(landmarks[33]),
#         normalizedLandmark_to_numpyVector(landmarks[468]),
#         normalizedLandmark_to_numpyVector(landmarks[133])
#     )
#     headVector = circ_tripoint_to_vector(
#         normalizedLandmark_to_numpyVector(landmarks[127]),
#         normalizedLandmark_to_numpyVector(landmarks[6]),
#         normalizedLandmark_to_numpyVector(landmarks[356])
#     )
#     return headVector

    
cap = cv2.VideoCapture(0)
while True:
    ret, fr = cap.read()
    frame = cv2.flip(fr, 1)
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
                cv2.circle(frame, (x, y), 1, (0,255,0), -1)

            # cv2.circle(frame, (int(landmarks.landmark[468].x * w), int(landmarks.landmark[468].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            # cv2.circle(frame, (int(landmarks.landmark[473].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            #left
            # cv2.circle(frame, (int(landmarks.landmark[70].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[LEFT_EYE_PUPIL].x * w), int(landmarks.landmark[LEFT_EYE_PUPIL].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[LEFT_EYE_TOP].x * w), int(landmarks.landmark[LEFT_EYE_TOP].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[LEFT_EYE_BOTTOM].x * w), int(landmarks.landmark[LEFT_EYE_BOTTOM].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            
            cv2.circle(frame, (int(landmarks.landmark[RIGHT_EYE_PUPIL].x * w), int(landmarks.landmark[RIGHT_EYE_PUPIL].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[RIGHT_EYE_TOP].x * w), int(landmarks.landmark[RIGHT_EYE_TOP].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[RIGHT_EYE_BOTTOM].x * w), int(landmarks.landmark[RIGHT_EYE_BOTTOM].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            # cv2.circle(frame, (int(landmarks.landmark[105].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            #right
            # cv2.circle(frame, (int(landmarks.landmark[374].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            # cv2.circle(frame, (int(landmarks.landmark[473].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            # cv2.circle(frame, (int(landmarks.landmark[386].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            # if (is_looking_at_screen(landmarks.landmark, w, h)):
            #     print("Looking")
            # else:
            #     print("Not looking")
            # print(calculate_eye_focus_rotation_pitch(landmarks.landmark))
            # print(isFocused(landmarks.landmark))
            if (isFocused(landmarks.landmark)):
                lastTrue = time.time()
                if time.time() - lastFalse >= 20:
                    print('looked away now!')
                    notification_sound = pygame.mixer.Sound('assets/notification.wav')
                    notification_sound.play()
            else:
                if time.time() - lastTrue >= 20:
                    print('looked away for 20 sec')
                    # Play notification sound
                    notification_sound = pygame.mixer.Sound('assets/done.wav')
                    notification_sound.play()
                    lastTrue = time.time()
                    lastFalse = time.time()
            


                
            # print(normalizedLandmark_to_numpyVector( landmarks.landmark[6] ))
            # print(calculate_eye_rotation())
            # depthTracking(landmarks)

            

            
            

            
    cv2.imshow('Eye Tracker', frame)
    #quite program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
