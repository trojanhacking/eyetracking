import cv2 #for display
import mediapipe as mp #for intelligence
import math
from utility import *
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def calculate_head_rotation(landmarks, w, h):
    left = landmarks[127]
    mid = landmarks[6]
    right = landmarks[356]
    return circ_tripoint_to_theta(left, mid, right)

def calculate_eye_rotation_left(landmarks, w, h): #left eye
    left = landmarks[33]
    mid = landmarks[468]
    right = landmarks[133]
    return circ_tripoint_to_theta(left, mid, right)

def calculate_eye_rotation_right(landmarks, w, h): #left eye
    left = landmarks[362]
    mid = landmarks[473]
    right = landmarks[263]
    return circ_tripoint_to_theta(left, mid, right)

def calculate_eye_focus_rotation(landmarks, w, h):
    return calculate_eye_rotation_left(landmarks, w, h) + calculate_eye_rotation_right(landmarks, w, h)

def circ_tripoint_to_theta(left, mid, right):
    """
    a = r * cos()
    b = r * sin()
    """
    a = (right.x - left.x) / 2
    b = ( (mid.x - left.x) - (right.x - mid.x ) ) / 2
    theta = math.atan(b/a)
    return theta

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

            #head
            cv2.circle(frame, (int(landmarks.landmark[127].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[6].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[356].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            # if (is_looking_at_screen(landmarks.landmark, w, h)):
            #     print("Looking")
            # else:
            #     print("Not looking")
            print(calculate_eye_focus_rotation(landmarks.landmark, w, h))
            # print(normalizedLandmark_to_numpyVector( landmarks.landmark[6] ))
            # print(calculate_eye_rotation())
            # depthTracking(landmarks)

            

            
            

            
    cv2.imshow('Eye Tracker', frame)
    #quite program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
