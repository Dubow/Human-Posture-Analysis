# utils/pose_utils.py
import math
import collections
import mediapipe as mp

HISTORY = collections.deque(maxlen=30)

def calculate_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x)
      - math.atan2(a.y - b.y, a.x - b.x)
    )
    return ang + 360 if ang < 0 else ang

def normalized_distance(p1, p2, ref):
    return math.hypot(p1.x - p2.x, p1.y - p2.y) / (ref or 1e-6)

def is_touching(p1, p2, ref, thresh=0.2):
    return normalized_distance(p1, p2, ref) < thresh

def detect_gestures(pose_landmarks, hand_landmarks=None, timestamp=None):
    gestures = []
    if not pose_landmarks:
        return gestures

    mp_pose = mp.solutions.pose
    lm      = pose_landmarks.landmark

    # Extract key points
    nose  = lm[mp_pose.PoseLandmark.NOSE.value]
    l_sh  = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    r_sh  = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    l_el  = lm[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    r_el  = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    l_wr  = lm[mp_pose.PoseLandmark.LEFT_WRIST.value]
    r_wr  = lm[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    l_hip = lm[mp_pose.PoseLandmark.LEFT_HIP.value]
    r_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
    l_ear = lm[mp_pose.PoseLandmark.LEFT_EAR.value]
    r_ear = lm[mp_pose.PoseLandmark.RIGHT_EAR.value]

    # Reference distance: shoulder width
    ref = math.hypot(l_sh.x - r_sh.x, l_sh.y - r_sh.y)

    # 1) Hands clasped (wrists together)
    if normalized_distance(l_wr, r_wr, ref) < 0.1 and abs(l_wr.y - r_wr.y) < 0.05:
        gestures.append("hands_clasped")

    # 2) Arms crossed
    arm_angle = calculate_angle(l_wr, l_el, r_wr)
    if 160 < arm_angle < 200 or (l_wr.x > r_el.x and r_wr.x < l_el.x):
        gestures.append("arms_crossed")

    # 3) Face touches
    if is_touching(l_wr, nose, ref) or is_touching(r_wr, nose, ref):
        gestures.append("touching_nose")
    m_l = lm[mp_pose.PoseLandmark.MOUTH_LEFT.value]
    m_r = lm[mp_pose.PoseLandmark.MOUTH_RIGHT.value]
    mouth_mid = type(nose)(x=(m_l.x + m_r.x)/2, y=(m_l.y + m_r.y)/2, z=0, visibility=0)
    if is_touching(l_wr, mouth_mid, ref) or is_touching(r_wr, mouth_mid, ref):
        gestures.append("touching_mouth")
    if is_touching(l_wr, m_l, ref) or is_touching(r_wr, m_r, ref):
        gestures.append("chin_stroking")

    # 4) Touching back of head
    back_head = type(nose)(
        x=(l_ear.x + r_ear.x)/2,
        y=(l_ear.y + r_ear.y)/2,
        z=0, visibility=0
    )
    if is_touching(l_wr, back_head, ref) or is_touching(l_wr, l_ear, ref):
        gestures.append("touching_back_head")
    if is_touching(r_wr, back_head, ref) or is_touching(r_wr, r_ear, ref):
        gestures.append("touching_back_head")

    # 5) Posture: sit straight vs lean
    hip_angle = calculate_angle(l_sh, l_hip, r_hip)
    if 170 < hip_angle < 190:
        gestures.append("sitting_up_straight")
    elif hip_angle < 160:
        gestures.append("leaning_forward")
    elif hip_angle > 200:
        gestures.append("leaning_back")

    # 6) Head tilt
    mid_sh = type(nose)(
        x=(l_sh.x + r_sh.x)/2, y=(l_sh.y + r_sh.y)/2, z=0, visibility=0
    )
    tilt = math.degrees(math.atan2(nose.y - mid_sh.y, nose.x - mid_sh.x))
    if abs(tilt) > 15:
        gestures.append("head_tilt")

    # 7) Head nod/shake (temporal)
    if timestamp is not None:
        HISTORY.append((timestamp, nose.x, nose.y))
        recent = [h for h in HISTORY if timestamp - h[0] < 1.0]
        ys     = [h[2] for h in recent]
        xs     = [h[1] for h in recent]
        if len(ys) >= 5 and max(ys)-min(ys) > 0.08:
            gestures.append("head_nod")
        if len(xs) >= 5 and max(xs)-min(xs) > 0.08:
            gestures.append("head_shake")

    return list(set(gestures))