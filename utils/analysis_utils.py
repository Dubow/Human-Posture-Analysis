# utils/analysis_utils.py
from config import gesture_meanings
from .llm_utils import analyze_gestures

def generate_analysis(gestures):
    if not gestures:
        return "No gestures detected."

    points = []
    for g in gestures:
        if g in gesture_meanings:
            m1, m2 = gesture_meanings[g]
            points.append(f"- **{g}**: {m1}; {m2}")
        if len(points) == 3:
            break

    if points:
        return "\n".join(points)
    return analyze_gestures(gestures)