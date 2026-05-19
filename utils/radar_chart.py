import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
rcParams['axes.unicode_minus'] = False

def create_radar_chart(result):

    labels = np.array([
        "高级感",
        "精致度",
        "气质感",
        "立体度",
        "亲和力"
    ])

    values = np.array([
        result["symmetry"] * 100,
        result["eye_ratio"] * 100,
        result["score"],
        result["ratio"] * 100,
        result["symmetry"] * 95
    ])

    # 闭合
    values = np.concatenate((values, [values[0]]))

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    )

    angles = np.concatenate((angles, [angles[0]]))

    # 创建图
    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw=dict(polar=True)
    )

    ax.plot(angles, values, linewidth=2)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels, fontsize=12)

    ax.set_ylim(0, 100)

    return fig