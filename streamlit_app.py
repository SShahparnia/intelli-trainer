import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from pose_utils import calculate_angle

st.set_page_config(page_title="IntelliTrainer", layout="centered")
st.title("IntelliTrainer: Fitness Motion & Repetition Tracker")
st.write("""
A minimal demo for bicep curls, shoulder press, pushups, and squats.\
Select an exercise and start your webcam to see live rep counting and angle!
""")

exercise = st.selectbox("Choose exercise", ["Bicep Curl", "Shoulder Press", "Pushup", "Squat"])
run = st.checkbox('Start Camera')

FRAME_WINDOW = st.image([])
rep_placeholder = st.empty()
angle_placeholder = st.empty()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

min_angle = 40
max_angle = 160
stage = None
rep_count = 0
# gooners
cap = None
if run:
    cap = cv2.VideoCapture(0)
    while run:
        ret, frame = cap.read()
        if not ret:
            st.warning("Camera not found.")
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        angle = 0
        try:
            landmarks = results.pose_landmarks.landmark
            if exercise == "Bicep Curl":
                l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
                if angle > max_angle:
                    stage = "down"
                if angle < min_angle and stage == "down":
                    stage = "up"
                    rep_count += 1
            elif exercise == "Shoulder Press":
                sp_r_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                sp_r_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                sp_r_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                sp_right_angle = calculate_angle(sp_r_shoulder, sp_r_elbow, sp_r_wrist)
                sp_l_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                sp_l_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                sp_l_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                sp_left_angle = calculate_angle(sp_l_shoulder, sp_l_elbow, sp_l_wrist)
                angle = (sp_right_angle + sp_left_angle) / 2
                if sp_right_angle > 150 and sp_left_angle > 150:
                    stage = "up"
                if sp_right_angle < 90 and sp_left_angle < 90 and stage == "up":
                    stage = "down"
                    rep_count += 1
            elif exercise == "Pushup":
                pu_r_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                pu_r_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                pu_r_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                pu_right_angle = calculate_angle(pu_r_shoulder, pu_r_elbow, pu_r_wrist)
                pu_l_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                pu_l_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                pu_l_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                pu_left_angle = calculate_angle(pu_l_shoulder, pu_l_elbow, pu_l_wrist)
                angle = (pu_right_angle + pu_left_angle) / 2
                if angle > 150:
                    stage = "up"
                if angle < 90 and stage == "up":
                    stage = "down"
                    rep_count += 1
            elif exercise == "Squat":
                r_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
                l_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                l_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                left_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
                angle = (right_knee_angle + left_knee_angle) / 2
                if angle > 160:
                    stage = "up"
                if angle < 100 and stage == "up":
                    stage = "down"
                    rep_count += 1
        except Exception:
            pass
        rep_placeholder.metric("Reps", rep_count)
        angle_placeholder.metric("Angle", int(angle))
        FRAME_WINDOW.image(rgb)
    cap.release()
