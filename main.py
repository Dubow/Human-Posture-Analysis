# main.py
import time
import cv2
import json
import os

import mediapipe as mp
from config import gesture_meanings, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT
from utils.pose_utils import detect_gestures
from utils.analysis_utils import generate_analysis

# Prepare output directories
os.makedirs("output/screenshots", exist_ok=True)
os.makedirs("output/coordinates", exist_ok=True)

# Initialize Mediapipe models
mp_pose    = mp.solutions.pose.Pose(min_detection_confidence=0.5)
mp_hands   = mp.solutions.hands.Hands(max_num_hands=2, min_detection_confidence=0.5)
mp_draw    = mp.solutions.drawing_utils
POSE_CONNS = mp.solutions.pose.POSE_CONNECTIONS
HAND_CONNS = mp.solutions.hands.HAND_CONNECTIONS


def save_frame_data(frame, idx, pose_lm, hand_lms):
    fn = f"{idx:04d}"
    frame = cv2.resize(frame, (SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))

    # Draw pose landmarks
    if pose_lm:
        mp_draw.draw_landmarks(frame, pose_lm, POSE_CONNS)
    # Draw hand landmarks
    if hand_lms:
        for h in hand_lms:
            mp_draw.draw_landmarks(frame, h, HAND_CONNS)

    # Save annotated screenshot
    img_path = f"output/screenshots/frame_{fn}.jpg"
    cv2.imwrite(img_path, frame)

    # Detect gestures & write JSON
    gestures = detect_gestures(pose_lm, hand_lms, timestamp=time.time())
    data = {"frame": idx, "gestures": gestures, "landmarks": []}
    if pose_lm:
        for i, lm in enumerate(pose_lm.landmark):
            data["landmarks"].append({
                "id": i,
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
                "v": lm.visibility
            })
    with open(f"output/coordinates/frame_{fn}.json", "w") as f:
        json.dump(data, f, indent=2)


def process_video(path="data/psychology video data.mp4", skip=10):
    cap = cv2.VideoCapture(path)
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_res  = mp_pose.process(rgb)
        hands_res = mp_hands.process(rgb)

        if idx % skip == 0:
            save_frame_data(frame, idx, pose_res.pose_landmarks, hands_res.multi_hand_landmarks)
        idx += 1

    cap.release()
    print(f"Processed {idx} frames.")


def analyze_saved(frame_idx):
    coord = f"output/coordinates/frame_{frame_idx:04d}.json"
    img   = f"output/screenshots/frame_{frame_idx:04d}.jpg"
    if not os.path.exists(coord):
        print("No data for that frame."); return

    with open(coord) as f:
        data = json.load(f)

    print(f"\n--- Frame {frame_idx} ---")
    for g in data["gestures"]:
        print(f" • {g}: {', '.join(gesture_meanings.get(g, ['Unknown']))}")

    print("\nAnalysis:")
    print(generate_analysis(data["gestures"]))

    img = cv2.imread(img)
    cv2.imshow(f"Frame {frame_idx}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("1) Process video")
    print("2) Analyze saved frame")
    choice = input("Choose (1/2): ").strip()
    if choice == "1":
        process_video()
    elif choice == "2":
        idx = int(input("Frame index: "))
        analyze_saved(idx)
    else:
        print("Invalid choice.")