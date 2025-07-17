# config.py

# Refined psychological meanings for each detected gesture
gesture_meanings = {
    # Hands & arms
    "hands_clasped":        ["excitement or anticipation", "eagerness to engage"],
    "arms_crossed":         ["defensive or guarded stance", "resistance to ideas"],

    # Head & face
    "touching_nose":        ["self‑soothing under stress", "uncertainty about next words"],
    "touching_mouth":       ["concealing emotions", "holding back information"],
    "chin_stroking":        ["weighing options", "deep thought"],
    "touching_back_head":   ["uncertainty", "self‑comfort while thinking"],
    "head_tilt":            ["active listening", "curiosity about topic"],
    "head_nod":             ["agreement or affirmation", "engaged response"],
    "head_shake":           ["skepticism", "disagreement"],

    # Posture
    "sitting_up_straight":  ["focus and attention", "readiness to participate"],
    "leaning_forward":      ["active engagement", "interest in speaker"],
    "leaning_back":         ["emotional distancing", "reservations about topic"],
    "slouching":            ["low energy", "lack of engagement"],
}

# Screenshot dimensions (optional)
SCREENSHOT_WIDTH  = 1280
SCREENSHOT_HEIGHT = 720