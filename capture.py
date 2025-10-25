import cv2
import mediapipe as mp

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


cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks: #each face
            for id, lm in enumerate(landmarks.landmark):
                h, w, _ = frame.shape
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 1, (0,255,0), -1)

            
            if (is_looking_at_screen(landmarks.landmark, w, h)):
                print("Looking")
            else:
                print("Not looking")
    
    cv2.imshow('Eye Tracker', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
