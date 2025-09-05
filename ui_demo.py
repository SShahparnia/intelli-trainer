import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IntelliTrainer UI')
        self.resize(900, 600)

        # Camera feed
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet('background: #222;')

        # Rep and angle info
        self.rep_label = QLabel('Reps: 0')
        self.rep_label.setAlignment(Qt.AlignLeft)
        self.rep_label.setStyleSheet('font-size: 20px; color: #0c0;')
        self.angle_label = QLabel('Angle: 0')
        self.angle_label.setAlignment(Qt.AlignLeft)
        self.angle_label.setStyleSheet('font-size: 20px; color: #09c;')

    info_layout = QVBoxLayout()
    info_layout.addWidget(self.rep_label)
    info_layout.addWidget(self.angle_label)
    info_layout.addStretch()

    main_layout = QHBoxLayout()
    main_layout.addLayout(info_layout)  # Info panel on the left
    main_layout.addWidget(self.image_label)  # Camera on the right
    self.setLayout(main_layout)

    self.cap = cv2.VideoCapture(0)
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_frame)
    self.timer.start(30)

    self.rep_count = 0
    self.angle = 0

    # --- Pose logic setup ---
    import mediapipe as mp
    from pose_utils import calculate_angle
    self.mp_pose = mp.solutions.pose
    self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    self.left_stage = None
    self.min_angle = 40
    self.max_angle = 160
    self.calculate_angle = calculate_angle

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_disp = rgb.copy()
        results = self.pose.process(rgb)

        try:
            landmarks = results.pose_landmarks.landmark
            # BICEP CURLS LOGIC (right arm, mirrored)
            l_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                       landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                       landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_angle = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
            self.angle = int(right_angle)
            if right_angle > self.max_angle:
                self.left_stage = "down"
            if right_angle < self.min_angle and self.left_stage == "down":
                self.left_stage = "up"
                self.rep_count += 1
        except Exception:
            pass

        h, w, ch = img_disp.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_disp.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))
        self.rep_label.setText(f'Reps: {self.rep_count}')
        self.angle_label.setText(f'Angle: {self.angle}')

   
    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CameraWidget()
    win.show()
    sys.exit(app.exec_())
