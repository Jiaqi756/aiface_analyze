import gradio as gr
from PIL import Image
import numpy as np
import cv2
import io

from utils.style_advisor import get_style_advice
from utils.report_generator import generate_report
from utils.style_classifier import classify_style
from utils.radar_chart import create_radar_chart
from utils.face_detect import detect_faces
from utils.landmark import draw_landmarks
from utils.beauty_analysis import analyze_face
from utils.poster_generator import generate_poster


# =========================
# 主分析函数
# =========================

def analyze(image):

    if image is None:
        return None, "请上传图片", None, None

    # PIL -> numpy
    image_np = np.array(image)

    # RGB -> BGR
    image_bgr = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2BGR
    )

    # =========================
    # 人脸检测
    # =========================

    faces = detect_faces(image_np)

    if len(faces) == 0:
        return None, "未检测到人脸", None, None

    # =========================
    # 画框
    # =========================

    draw_img = image_bgr.copy()

    for face in faces:

        # 兼容 insightface dict
        if isinstance(face, dict):
            bbox = np.array(face["bbox"]).astype(int)
        else:
            bbox = face.bbox.astype(int)

        x1, y1, x2, y2 = bbox

        cv2.rectangle(
            draw_img,
            (x1, y1),
            (x2, y2),
            (255, 0, 255),
            3
        )

    # =========================
    # Landmark
    # =========================

    landmark_image = draw_landmarks(draw_img)

    landmark_image = cv2.cvtColor(
        landmark_image,
        cv2.COLOR_BGR2RGB
    )

    # =========================
    # 美学分析
    # =========================

    result = analyze_face(image_bgr)

    if result is None:
        return landmark_image, "分析失败", None, None

    # =========================
    # 风格分析
    # =========================

    style_results = classify_style(image_bgr)

    # =========================
    # AI 报告
    # =========================

    report = generate_report(
        result,
        style_results
    )

    # =========================
    # 风格推荐
    # =========================

    top_style = style_results[0]["label"]

    advice = get_style_advice(top_style)

    advice_text = f"""
【AI识别风格】
{top_style}

【发型推荐】
- {"\n- ".join(advice["hair"])}

【妆容推荐】
- {"\n- ".join(advice["makeup"])}

【穿搭推荐】
- {"\n- ".join(advice["fashion"])}
"""

    # =========================
    # 海报生成
    # =========================

    poster = generate_poster(
        landmark_image,
        result,
        style_results,
        report
    )

    # =========================
    # 雷达图
    # =========================

    fig = create_radar_chart(result)

    return (
        landmark_image,
        report + "\n\n" + advice_text,
        fig,
        poster
    )


# =========================
# Gradio UI
# =========================

with gr.Blocks(title="AI Face Analyzer") as demo:

    gr.Markdown(
        """
# ✨ AI 面部美学分析系统

上传照片，进行 AI 审美分析
"""
    )

    with gr.Row():

        input_image = gr.Image(
            type="pil",
            label="上传照片"
        )

    analyze_btn = gr.Button("开始分析")

    output_image = gr.Image(
        label="人脸关键点分析"
    )

    output_text = gr.Textbox(
        label="AI 分析报告",
        lines=18
    )

    output_chart = gr.Plot(
        label="气质雷达图"
    )

    output_poster = gr.Image(
        label="AI 海报"
    )

    analyze_btn.click(
        fn=analyze,
        inputs=input_image,
        outputs=[
            output_image,
            output_text,
            output_chart,
            output_poster
        ]
    )

# =========================
# 启动
# =========================

demo.launch()
