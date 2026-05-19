def get_style_advice(top_style):

    advice = {}

    # ===== 港风 =====

    if top_style == "港风美女":

        advice["hair"] = [
            "港风大波浪",
            "黑长直",
            "偏分卷发"
        ]

        advice["makeup"] = [
            "红棕色口红",
            "立体修容",
            "复古眼线"
        ]

        advice["fashion"] = [
            "复古港风",
            "黑色系穿搭",
            "西装风格"
        ]

    # ===== 清冷 =====

    elif top_style == "清冷感":

        advice["hair"] = [
            "黑长直",
            "低层次长发",
            "中分发型"
        ]

        advice["makeup"] = [
            "低饱和妆容",
            "冷调口红",
            "轻眼妆"
        ]

        advice["fashion"] = [
            "极简高级风",
            "灰黑白穿搭",
            "韩系清冷风"
        ]

    # ===== 甜妹 =====

    elif top_style == "甜妹":

        advice["hair"] = [
            "空气刘海",
            "羊毛卷",
            "双马尾"
        ]

        advice["makeup"] = [
            "粉色系腮红",
            "水光唇",
            "卧蚕妆"
        ]

        advice["fashion"] = [
            "日系软妹风",
            "浅色系穿搭",
            "学院风"
        ]

    # ===== 默认 =====

    else:

        advice["hair"] = [
            "自然中长发",
            "微卷发",
            "层次短发"
        ]

        advice["makeup"] = [
            "自然裸妆",
            "轻修容",
            "干净底妆"
        ]

        advice["fashion"] = [
            "简约风",
            "基础款穿搭",
            "日常高级感"
        ]

    return advice