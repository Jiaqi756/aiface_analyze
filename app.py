import streamlit as st
from PIL import Image
import numpy as np
import cv2
import time
import io

from utils.style_advisor import get_style_advice
from utils.report_generator import generate_report
from utils.style_classifier import classify_style
from utils.radar_chart import create_radar_chart
from utils.face_detect import detect_faces
from utils.landmark import draw_landmarks
from utils.beauty_analysis import analyze_face
from utils.poster_generator import generate_poster

# ================= 页面设置 =================

st.set_page_config(
    page_title="AI Face Analyzer",
    page_icon="✨",
    layout="centered"
)

# ================= 页面美化 =================

st.markdown("""
<style>

/* 整体背景 */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f7ff,
        #efe8ff
    );
}

/* 页面间距 */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 850px;
}

/* 标题 */
h1 {
    color: #7c4dff;
    text-align: center;
    font-size: 2.2rem !important;
    font-weight: 700;
}

/* 小标题 */
h2, h3 {
    color: #5e35b1;
}

/* 正文 */
.stMarkdown {
    font-size: 16px;
}

/* 卡片 */
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* 风格标签 */
.style-tag {
    display: inline-block;
    background-color: #7c4dff;
    color: white;
    padding: 8px 14px;
    border-radius: 20px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 14px;
}

/* 手机适配 */
@media (max-width: 768px) {

    h1 {
        font-size: 1.8rem !important;
    }

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

}

</style>
""", unsafe_allow_html=True)

# ================= 标题 =================

st.title("✨ AI 面部美学分析系统")

st.markdown(
    "<div style='text-align:center;color:gray;'>"
    "上传一张照片，开始 AI 审美分析"
    "</div>",
    unsafe_allow_html=True
)

st.write("")

# ================= 上传图片 =================

uploaded_file = st.file_uploader(
    "请上传图片",
    type=["jpg", "jpeg", "png"]
)

# ================= 开始分析 =================

if uploaded_file is not None:

    # 读取图片
    image = Image.open(uploaded_file).convert("RGB")

    image_np = np.array(image)

    image_bgr = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2BGR
    )

    # ================= 人脸检测 =================

    with st.spinner("🔍 正在检测人脸..."):

        time.sleep(1)

        faces = detect_faces(image_np)

    # 画框
    for face in faces:

        bbox = face.bbox.astype(int)

        x1, y1, x2, y2 = bbox

        cv2.rectangle(
            image_bgr,
            (x1, y1),
            (x2, y2),
            (255, 0, 255),
            3
        )

    # ================= Landmark =================

    with st.spinner("🧠 正在分析面部关键点..."):

        time.sleep(1)

        landmark_image = draw_landmarks(image_bgr)

    landmark_image = cv2.cvtColor(
        landmark_image,
        cv2.COLOR_BGR2RGB
    )

    # ================= 图片展示 =================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image(
        landmark_image,
        caption=f"检测到 {len(faces)} 张人脸",
        use_container_width=True
    )

    st.success("AI 面部关键点检测完成！")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= 美学分析 =================

    with st.spinner("📊 正在计算面部比例..."):

        time.sleep(1)

        result = analyze_face(image_bgr)

    if result:

        # ================= AI评分 =================

        st.subheader("📊 AI 面部美学分析")

        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.metric(
                "综合评分",
                result["score"]
            )

        with row1_col2:
            st.metric(
                "宽高比",
                result["ratio"]
            )

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            st.metric(
                "眼距比例",
                result["eye_ratio"]
            )

        with row2_col2:
            st.metric(
                "对称性",
                result["symmetry"]
            )

        # ================= 雷达图 =================

        st.subheader("🎯 AI 气质雷达图")

        fig = create_radar_chart(result)

        st.pyplot(fig)

        # ================= 风格识别 =================

        st.subheader("🎨 AI 风格分析")

        with st.spinner("🎨 正在识别审美风格..."):

            time.sleep(2)

            style_results = classify_style(image_bgr)

        style_html = ""

        for item in style_results[:5]:

            style_html += f"""
            <span class="style-tag">
                {item['label']} {item['score']}%
            </span>
            """

        st.markdown(style_html, unsafe_allow_html=True)

        # ================= AI报告 =================

        st.subheader("📝 AI 审美分析报告")

        with st.spinner("✨ 正在生成 AI 审美报告..."):

            time.sleep(1)

            report = generate_report(
                result,
                style_results
            )

        st.markdown(f"""
        <div class="card" style="
            line-height:2;
            font-size:17px;
        ">
        {report}
        </div>
        """, unsafe_allow_html=True)

        # ================= 风格推荐 =================

        st.subheader("💄 AI 风格推荐")

        top_style = style_results[0]["label"]

        advice = get_style_advice(top_style)

        # 发型
        st.markdown("""
        <div class="card">
        <h3>💇 发型推荐</h3>
        """, unsafe_allow_html=True)

        for item in advice["hair"]:

            st.write(f"• {item}")

        st.markdown("</div>", unsafe_allow_html=True)

        # 妆容
        st.markdown("""
        <div class="card">
        <h3>💋 妆容推荐</h3>
        """, unsafe_allow_html=True)

        for item in advice["makeup"]:

            st.write(f"• {item}")

        st.markdown("</div>", unsafe_allow_html=True)

        # 穿搭
        st.markdown("""
        <div class="card">
        <h3>👗 穿搭推荐</h3>
        """, unsafe_allow_html=True)

        for item in advice["fashion"]:

            st.write(f"• {item}")

        st.markdown("</div>", unsafe_allow_html=True)

        # ================= AI 海报生成 =================

        st.subheader("📸 AI 分析海报")

        with st.spinner("✨ 正在生成 AI 海报..."):

            time.sleep(2)

            poster = generate_poster(
                landmark_image,
                result,
                style_results,
                report
            )

        # 显示海报
        '''
        st.image(
            poster,
            caption="AI 审美分析海报",
            use_container_width=True
        )
        '''
        # 下载按钮
        import io

        buf = io.BytesIO()

        poster.save(buf, format="PNG")

        byte_im = buf.getvalue()

        st.download_button(
            label="📥 下载 AI 海报",
            data=byte_im,
            file_name="ai_face_poster.png",
            mime="image/png",
            use_container_width=True
        )