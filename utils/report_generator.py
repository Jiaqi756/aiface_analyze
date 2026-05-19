def generate_report(result, style_results):

    score = result["score"]

    symmetry = result["symmetry"]

    ratio = result["ratio"]

    top_style = style_results[0]["label"]

    report = []

    # ===== 综合评价 =====

    if score >= 85:
        report.append("你的整体面部协调度非常高，属于比较有高级感的类型。")

    elif score >= 75:
        report.append("你的五官比例较协调，整体颜值表现比较优秀。")

    else:
        report.append("你的面部结构具有一定个人特色，风格辨识度较高。")

    # ===== 对称性 =====

    if symmetry > 0.9:
        report.append("你的面部对称性较好，会让整体气质更加自然耐看。")

    elif symmetry > 0.8:
        report.append("你的面部整体比较协调，视觉平衡感不错。")

    # ===== 脸型 =====

    if ratio > 0.8:
        report.append("你的脸型偏修长，更容易呈现高级感和镜头感。")

    elif ratio > 0.7:
        report.append("你的脸型比例较均衡，属于比较大众接受度高的类型。")

    else:
        report.append("你的面部轮廓偏柔和，容易给人亲和感。")

    # ===== 风格 =====

    report.append(f"你的整体风格更偏「{top_style}」路线。")

    # ===== 风格建议 =====

    if top_style == "港风美女":
        report.append("比较适合浓眉、立体妆容以及复古风穿搭。")

    elif top_style == "清冷感":
        report.append("更适合低饱和妆容与简洁高级风格。")

    elif top_style == "甜妹":
        report.append("更适合轻妆感和温柔系穿搭风格。")

    elif top_style == "御姐风":
        report.append("适合强调气场感和轮廓感的造型。")

    return "\n".join(report)