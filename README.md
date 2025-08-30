# IntelliTrainer: Bicep Curl Repetition Tracker

A lightweight real-time computer vision app using MediaPipe and OpenCV to track **bicep curls and hammer curls** for both arms using your webcam.

Designed to run efficiently on macOS (Intel-based) with no GPU required.

> **Note:** Current functionality is limited to **bicep motion tracking only**. Support for full-body workouts (e.g., squats, push-ups, shoulder presses) is under development.

---

## Features

- Tracks left and right arms independently
- Works from front-facing or side-facing views
- Uses elbow joint angle to detect rep cycles
- Real-time feedback overlay on camera feed

---

## Requirements

- Python 3.11+
- Virtual environment (recommended)
- Webcam

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the App

```bash
python main.py
```

Press `Q` to quit the window.

---

## Project Structure

```
intelli_trainer/
├── main.py              # Main script for pose tracking and rep counting
├── pose_utils.py        # Helper to calculate joint angles
├── requirements.txt     # Python dependencies
└── README.md
```

---

## How It Works

- Uses MediaPipe Pose to extract body landmarks
- Calculates elbow angle for each arm (shoulder–elbow–wrist)
- Counts a rep when the arm fully contracts and returns to rest

---

