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


            # MIRRORED CAMERA: Swap left/right logic
            # LEFT ARM (actually user's right)
            l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)

            # RIGHT ARM (actually user's left)
            r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

            # RIGHT rep logic (user's right arm)
            if right_angle > max_angle:
                right_stage = "down"
            if right_angle < min_angle and right_stage == "down":
                right_stage = "up"
                right_count += 1

            # LEFT rep logic (user's left arm)
            if left_angle > max_angle:
                left_stage = "down"
            if left_angle < min_angle and left_stage == "down":
                left_stage = "up"
                left_count += 1

            cv2.putText(image, f'Left: {int(left_angle)}°', (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(image, f'Right: {int(right_angle)}°', (20, 140),
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

cap.release()
cv2.destroyAllWindows()
