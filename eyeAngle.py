from constants import *

def calculate_head_rotation(landmarks):
    left = landmarks[127]
    mid = landmarks[6]
    right = landmarks[356]
    return circ_tripoint_to_theta(left.x, mid.x, right.x)

def calculate_eye_rotation_left(landmarks): #left eye
    left = landmarks[33]
    mid = landmarks[468]
    right = landmarks[133]
    return circ_tripoint_to_theta(left.x, mid.x, right.x)

def calculate_eye_rotation_right(landmarks): #left eye
    left = landmarks[362]
    mid = landmarks[473]
    right = landmarks[263]
    return circ_tripoint_to_theta(left.x, mid.x, right.x)

def calculate_eye_focus_rotation(landmarks):
    return calculate_eye_rotation_left(landmarks) + calculate_eye_rotation_right(landmarks) + calculate_head_rotation(landmarks) / 1.5

def isFocused(landmarks):
    offset = 0.2
    print(abs(calculate_eye_focus_rotation_pitch(landmarks)) - offset, end=";")
    return (abs(calculate_eye_focus_rotation(landmarks)) < MAX_HORIZONTAL_THETA) and (abs(calculate_eye_focus_rotation_pitch(landmarks) - offset) < MAX_PITCH_THETA)

def calculate_eye_rotation_left_pitch(landmarks): #left eye
    left = landmarks[LEFT_EYE_BOTTOM]
    mid = landmarks[LEFT_EYE_PUPIL]
    right = landmarks[LEFT_EYE_TOP]
    return circ_tripoint_to_theta(left.y, mid.y, right.y)

def calculate_eye_rotation_right_pitch(landmarks): #left eye
    left = landmarks[RIGHT_EYE_BOTTOM]
    mid = landmarks[RIGHT_EYE_PUPIL]
    right = landmarks[RIGHT_EYE_TOP]
    return circ_tripoint_to_theta(left.y, mid.y, right.y)

def calculate_head_rotation_pitch(landmarks):
    left = landmarks[127]
    mid = landmarks[6]
    right = landmarks[356]
    return circ_tripoint_to_theta(left.y, mid.y, right.y)

def calculate_eye_focus_rotation_pitch(landmarks):
    return (calculate_eye_rotation_left_pitch(landmarks) + calculate_eye_rotation_right_pitch(landmarks)) / 2

def circ_tripoint_to_theta(left, mid, right):
    import math
    a = (right - left) / 2
    b = ( (mid - left) - (right - mid) ) / 2
    theta = math.atan(b/a)
    return theta