
# Human Posture and Gesture Analysis

A Python-based computer vision research prototype for extracting human pose landmarks, detecting body gestures, and generating descriptive interpretations from video recordings.

Developed during a summer research experience at Harbin Institute of Technology (HIT) in 2025.

## Overview

This project explores how computer vision can be used to identify observable body postures and gestures from video data.

It combines OpenCV and MediaPipe with rule-based geometric calculations to detect patterns involving body posture, hand positioning, and head movements.

The project was developed as a research prototype and is not a validated psychological assessment system.

## Features

- Video processing using OpenCV
- Pose and hand landmark estimation using MediaPipe
- Rule-based posture and gesture detection
- Frame-by-frame landmark extraction
- Annotated image generation
- JSON output containing landmark coordinates and detected gestures
- Descriptive gesture interpretation
- Optional GPT-2 text-generation fallback

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy (indirectly through dependencies)
- Hugging Face Transformers
- PyTorch

## Project Structure

```text
Human-Posture-Analysis/
├── main.py
├── config.py
├── requirements.txt
├── data/
│   └── psychology video data.mp4
├── utils/
│   ├── pose_utils.py
│   ├── analysis_utils.py
│   └── llm_utils.py
└── output/               # Generated at runtime
    ├── screenshots/
    └── coordinates/
```

## How It Works

### 1. Video Input

The system reads a video using OpenCV.

### 2. Landmark Detection

MediaPipe estimates human body landmarks and hand landmarks.

### 3. Gesture Detection

The system applies geometric heuristics, including normalized distances, joint angles, and changes in landmark positions over time.

Examples of gesture labels include:

- Hands clasped
- Arms crossed
- Touching the nose or mouth
- Head tilting
- Head nodding or shaking
- Leaning forward or backward

The detectors are experimental and may produce false positives.

### 4. Output Generation

The system saves:

- Annotated frames in `output/screenshots/`
- Landmark coordinates and gesture labels in `output/coordinates/`

### 5. Descriptive Analysis

Detected gestures are mapped to predefined descriptions.

An optional GPT-2 fallback is present in the code for gestures without predefined descriptions. It is not a trained psychological classifier.

## Installation

Clone the repository:

```bash
git clone https://github.com/Dubow/Human-Posture-Analysis.git
cd Human-Posture-Analysis
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Note: MediaPipe and the other dependencies may require compatible Python versions. The project has not been verified against every current dependency release.

## Usage

Run:

```bash
python main.py
```

Select:

**1 — Process video**

Processes `data/psychology video data.mp4` and saves outputs at every tenth frame by default.

**2 — Analyze saved frame**

Enter a previously saved frame index to display its recorded gesture labels, descriptive analysis, and annotated image.

For example, after processing a video, frame `0010` may be available.

## Research Scope and Limitations

This implementation is a prototype intended to explore computer vision and geometric gesture detection.

Important limitations include:

- Gesture detection relies on hand-crafted thresholds.
- Detection quality depends on pose visibility, camera angle, and video quality.
- Some posture and head-movement rules are experimental.
- Hand landmarks are estimated, but the current gesture rules rely primarily on pose landmarks.
- Behavioral descriptions should not be interpreted as reliable evidence of emotion, intention, or psychological state.
- No benchmark accuracy, precision, recall, or validated research results are claimed.

## Future Improvements

Possible directions include:

- Improved temporal gesture detection
- Better use of hand landmarks
- Confidence-based gesture filtering
- Quantitative evaluation against annotated video datasets
- More robust posture-angle calculations
- Reproducible tests and dependency pinning

## Academic Context

Developed as part of a 2025 summer research experience at Harbin Institute of Technology, involving computer vision, landmark extraction, gesture analysis, and visualization.

## Author

Abdirahman Dubow

