import cv2
import mediapipe as mp
import

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def is_looking_at_screen(landmarks, w, h):
    left_iris = landmarks[468]  # MediaPipe iris landmark
    left_eye_left = landmarks[33]
    left_eye_right = landmarks[133]

    iris_x = left_iris.x
    eye_left_x = left_eye_left.x
    eye_right_x = left_eye_right.x

    ratio = (iris_x - eye_left_x) / (eye_right_x - eye_left_x)
    return 0.35 < ratio < 0.65  # threshold range for "centered" gaze

def calculate_headd_rotation(landmarks, w, h):
    left = landmarks[127]
    mid = landmarks[6]
    right = landmarks[356]
    return circ_tripoint_to_theta(left, mid, right)

def calculate_eye_rotation(landmarks, w, h):
    left = landmarks[33]
    mid = landmarks[468]
    right = landmarks[133]
    return circ_tripoint_to_theta(left, mid, right)

def circ_tripoint_to_theta(left, mid, right):
    """
    a = r * cos()
    b = r * sin()
    """
    a = (right.x - left.x) / 2
    b = ( (mid.x - left.x) - (right.x - mid.x ) ) / 2
    theta = math.atan(b/a)
    return theta


class Worker()
cap = cv2.VideoCapture(0)
while True:
    ret, fr = cap.read()
    frame = cv2.flip(fr, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks: #each face
            h, w, _ = frame.shape
            for id, lm in enumerate(landmarks.landmark):
                
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 1, (0,255,0), -1)

            cv2.circle(frame, (int(landmarks.landmark[468].x * w), int(landmarks.landmark[468].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[473].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            #head
            cv2.circle(frame, (int(landmarks.landmark[127].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[6].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (int(landmarks.landmark[356].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

            # if (is_looking_at_screen(landmarks.landmark, w, h)):
            #     print("Looking")
            # else:
            #     print("Not looking")
            print(calculate_eye_rotation(landmarks.landmark, w, h))
    
    cv2.imshow('Eye Tracker', frame)
    #quite program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
