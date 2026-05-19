from insightface.app import FaceAnalysis
import cv2

# 初始化模型
app = FaceAnalysis(name='buffalo_l')

app.prepare(ctx_id=0)

def detect_faces(image):

    # 转 BGR
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 人脸检测
    faces = app.get(img)

    return faces