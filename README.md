
# IntelliTrainer: Fitness Motion & Repetition Tracker

A lightweight real-time computer vision app using MediaPipe and OpenCV to track **bicep curls, shoulder presses, pushups, and squats** for both arms/legs using your webcam.

> **Note:** The app now supports bicep curls, shoulder presses, pushups, and squats. Future progress will include more functional exercises such as pullup types (archer, typewriter, one arm, two arm, close, wide, normal grip, etc).

---


## Features

- Tracks bicep curls, shoulder presses, pushups, and squats
- Tracks left and right arms independently (for arm-based exercises)
- Works from front-facing or side-facing views
- Uses joint angles (elbow, knee) to detect rep cycles
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
- Calculates joint angles (elbow for arms, knee for squats)
- Counts a rep when the limb fully contracts and returns to rest/extension
- Displays real-time rep counts for each exercise on the camera feed

---

## Roadmap / Future Progress

- Add support for more functional exercises, especially pullup types:
	- Archer pullup
	- Typewriter pullup
	- One arm pullup
	- Two arm pullup
	- Close grip pullup
	- Wide grip pullup
	- Normal grip pullup
	- ...and more!

---

