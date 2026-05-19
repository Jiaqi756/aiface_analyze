from insightface.app import FaceAnalysis
import cv2

# 初始化模型
app = FaceAnalysis(
    name='buffalo_l',
    providers=['CPUExecutionProvider']
)

# CPU模式
app.prepare(ctx_id=-1)

def detect_faces(image):

    # RGB -> BGR
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 人脸检测
    faces = app.get(img)

    return faces
