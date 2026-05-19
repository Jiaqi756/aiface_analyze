import clip
import torch
from PIL import Image
import cv2

# 使用CPU
device = "cpu"

# 加载模型
model, preprocess = clip.load("ViT-B/32", device=device)

# 风格标签
style_labels = [
    "高级脸",
    "清冷感",
    "甜妹",
    "港风美女",
    "御姐风",
    "邻家感",
    "韩系气质",
    "氛围感美女"
]

def classify_style(image_bgr):

    # 转RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # PIL格式
    pil_image = Image.fromarray(image_rgb)

    # 预处理
    image_input = preprocess(pil_image).unsqueeze(0).to(device)

    # 文本
    text = clip.tokenize(style_labels).to(device)

    # 推理
    with torch.no_grad():

        logits_per_image, _ = model(image_input, text)

        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

    # 排序
    results = []

    for label, prob in zip(style_labels, probs):

        results.append({
            "label": label,
            "score": round(float(prob) * 100, 1)
        })

    # 按概率排序
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results