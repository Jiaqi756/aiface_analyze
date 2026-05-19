from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def generate_poster(
    image_rgb,
    result,
    style_results,
    report
):

    # 海报尺寸
    width = 800
    height = 1400

    poster = Image.new(
        "RGB",
        (width, height),
        (245, 247, 255)
    )

    draw = ImageDraw.Draw(poster)

    # 字体
    title_font = ImageFont.truetype(
        "assets/msyh.ttc",
        42
    )

    text_font = ImageFont.truetype(
        "assets/msyh.ttc",
        28
    )

    small_font = ImageFont.truetype(
        "assets/msyh.ttc",
        22
    )

    # ===== 标题 =====

    draw.text(
        (220, 40),
        "AI 面部美学分析报告",
        fill=(90, 60, 180),
        font=title_font
    )

    # ===== 用户图片 =====

    image_pil = Image.fromarray(image_rgb)

    image_pil = image_pil.resize((500, 500))

    poster.paste(image_pil, (150, 120))

    # ===== 综合评分 =====

    draw.text(
        (80, 660),
        f"综合评分：{result['score']}",
        fill=(0,0,0),
        font=text_font
    )

    # ===== 风格标签 =====

    top_styles = [
        item["label"]
        for item in style_results[:3]
    ]

    style_text = " / ".join(top_styles)

    draw.text(
        (80, 730),
        f"AI 风格：{style_text}",
        fill=(120,80,200),
        font=text_font
    )

    # ===== AI 报告 =====

    report_lines = report.split("。")

    y = 820

    draw.text(
        (80, y),
        "AI 审美分析：",
        fill=(0,0,0),
        font=text_font
    )

    y += 60

    for line in report_lines:

        if len(line.strip()) > 0:

            draw.text(
                (100, y),
                "• " + line.strip(),
                fill=(60,60,60),
                font=small_font
            )

            y += 50

    return poster