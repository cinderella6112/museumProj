from agent import ask_museum_agent

# from __future__ import annotations

# 各省示例博物馆与旅行提示（演示数据，可替换为知识库查询结果）
'''PROVINCE_MUSEUMS: dict[str, list[str]] = {
    "beijing": ["故宫博物院", "中国国家博物馆", "首都博物馆", "中国科技馆"],
    "shanghai": ["上海博物馆", "中华艺术宫", "上海自然博物馆"],
    "zhejiang": ["浙江省博物馆", "中国丝绸博物馆", "良渚博物院"],
    "shaanxi": ["陕西历史博物馆", "秦始皇兵马俑博物馆", "西安碑林博物馆"],
    "sichuan": ["四川博物院", "三星堆博物馆", "成都博物馆"],
    "guangdong": ["广东省博物馆", "南越王博物院", "深圳博物馆"],
}

DEFAULT_MUSEUMS = ["当地综合性博物馆", "省级博物馆", "专题博物馆（艺术/自然/历史）"]'''


def generate_reply(province_code: str, province_name: str, message: str) -> tuple[str, list[str]]:
    '''museums = PROVINCE_MUSEUMS.get(province_code, DEFAULT_MUSEUMS)
    museum_list = "、".join(museums[:4])

    reply = (
        f"您好！我是{province_name}博物馆旅行助手。\n\n"
        f"根据您的问题「{message}」，为您推荐以下博物馆：{museum_list}。\n\n"
        f"**建议行程（1-2天）**\n"
        f"1. 上午：参观核心展馆（预留 2-3 小时）\n"
        f"2. 下午：游览相邻文化街区或第二座专题馆\n"
        f"3. 交通：优先地铁/公交；热门场馆建议提前网上预约门票\n\n"
        f"如需更详细的路线、开放时间与亲子/研学主题安排，请继续告诉我您的出行日期、"
        f"人数和兴趣偏好（历史/艺术/科技等）。"
    )

    suggestions = [
        "帮我规划周末两天的博物馆路线",
        "有哪些适合亲子游的博物馆？",
        "热门博物馆需要预约吗？",
    ]
    return reply, suggestions'''

    return ask_museum_agent(message)
