import mediapipe as mp
import numpy as np
import cv2

# 初始化
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True
)

def analyze_face(image):

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        return None

    face_landmarks = results.multi_face_landmarks[0]

    h, w, _ = image.shape

    # 转成像素坐标
    points = []

    for lm in face_landmarks.landmark:

        x = int(lm.x * w)
        y = int(lm.y * h)

        points.append((x, y))

    # ===== 关键点 =====

    forehead = points[10]
    chin = points[152]

    left_face = points[234]
    right_face = points[454]

    left_eye = points[33]
    right_eye = points[263]

    nose = points[1]

    # ===== 面部长宽 =====

    face_height = np.linalg.norm(
        np.array(forehead) - np.array(chin)
    )

    face_width = np.linalg.norm(
        np.array(left_face) - np.array(right_face)
    )

    ratio = face_width / face_height

    # ===== 眼距 =====

    eye_distance = np.linalg.norm(
        np.array(left_eye) - np.array(right_eye)
    )

    eye_ratio = eye_distance / face_width

    # ===== 对称性（简化版）=====

    center_x = nose[0]

    left_dist = abs(left_face[0] - center_x)
    right_dist = abs(right_face[0] - center_x)

    symmetry = 1 - abs(left_dist - right_dist) / face_width

    # ===== 综合评分 =====

    score = (
        symmetry * 40 +
        (1 - abs(ratio - 0.75)) * 30 +
        eye_ratio * 30
    )

    score = max(0, min(100, score))

    return {
        "score": round(score, 1),
        "ratio": round(ratio, 2),
        "eye_ratio": round(eye_ratio, 2),
        "symmetry": round(symmetry, 2)
    }