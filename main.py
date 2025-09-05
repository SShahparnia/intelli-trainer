import cv2
import numpy as np
import mediapipe as mp
from pose_utils import calculate_angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

left_count = 0
right_count = 0
left_stage = None
right_stage = None

min_angle = 40
max_angle = 160

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # BICEP CURLS LOGIC
            l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)

            r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

            if right_angle > max_angle:
                right_stage = "down"
            if right_angle < min_angle and right_stage == "down":
                right_stage = "up"
                right_count += 1

            if left_angle > max_angle:
                left_stage = "down"
            if left_angle < min_angle and left_stage == "down":
                left_stage = "up"
                left_count += 1

            cv2.putText(image, f'Left: {int(left_angle)}', (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(image, f'Right: {int(right_angle)}', (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        except:
            pass

        cv2.putText(image, f'Reps (L): {left_count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f'Reps (R): {right_count}', (300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Bicep Curls Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


# --- Additional Exercise Logic ---
shoulder_press_count = 0
shoulder_press_stage = None
pushup_count = 0
pushup_stage = None
squat_count = 0
squat_stage = None

def get_landmark_xy(landmarks, landmark):
    return [landmarks[landmark.value].x, landmarks[landmark.value].y]

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # SHOULDER PRESS LOGIC
            sp_r_shoulder = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
            sp_r_elbow = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
            sp_r_wrist = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
            sp_right_angle = calculate_angle(sp_r_shoulder, sp_r_elbow, sp_r_wrist)
            sp_l_shoulder = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
            sp_l_elbow = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW)
            sp_l_wrist = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
            sp_left_angle = calculate_angle(sp_l_shoulder, sp_l_elbow, sp_l_wrist)

            if sp_right_angle > 150 and sp_left_angle > 150:
                shoulder_press_stage = "up"
            if sp_right_angle < 90 and sp_left_angle < 90 and shoulder_press_stage == "up":
                shoulder_press_stage = "down"
                shoulder_press_count += 1

            # PUSHUP LOGIC
            pu_r_shoulder = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
            pu_r_elbow = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
            pu_r_wrist = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
            pu_right_angle = calculate_angle(pu_r_shoulder, pu_r_elbow, pu_r_wrist)
            pu_l_shoulder = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
            pu_l_elbow = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW)
            pu_l_wrist = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
            pu_left_angle = calculate_angle(pu_l_shoulder, pu_l_elbow, pu_l_wrist)
            pu_avg_angle = (pu_right_angle + pu_left_angle) / 2
            if pu_avg_angle > 150:
                pushup_stage = "up"
            if pu_avg_angle < 90 and pushup_stage == "up":
                pushup_stage = "down"
                pushup_count += 1

            # SQUAT LOGIC
            r_hip = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
            r_knee = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
            r_ankle = get_landmark_xy(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
            right_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
            l_hip = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
            l_knee = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
            l_ankle = get_landmark_xy(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
            left_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
            squat_avg_angle = (right_knee_angle + left_knee_angle) / 2
            if squat_avg_angle > 160:
                squat_stage = "up"
            if squat_avg_angle < 100 and squat_stage == "up":
                squat_stage = "down"
                squat_count += 1

            # DISPLAY COUNTS
            cv2.putText(image, f'Shoulder Press: {shoulder_press_count}', (20, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(image, f'Pushups: {pushup_count}', (20, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
            cv2.putText(image, f'Squats: {squat_count}', (20, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        except:
            pass

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Bicep Curls Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
