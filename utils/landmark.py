import mediapipe as mp
import cv2

# 初始化 FaceMesh
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# 绘图工具
mp_drawing = mp.solutions.drawing_utils

# 绘图样式
drawing_spec = mp_drawing.DrawingSpec(
    thickness=1,
    circle_radius=1
)

def draw_landmarks(image):

    # 转RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 检测
    results = face_mesh.process(rgb_image)

    # 复制图片
    output_image = image.copy()

    # 如果检测到人脸
    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # 绘制关键点
            mp_drawing.draw_landmarks(
                image=output_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

    return output_image