"""生成中文模拟评论数据"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


# 正向评论模板
POSITIVE_TEMPLATES = [
    "功能强大，{pos_detail}，非常满意！",
    "界面简洁，{pos_detail}，推荐购买。",
    "性价比很高，{pos_detail}，物超所值。",
    "用了两周了，{pos_detail}，好评。",
    "{pos_detail}，做工精致，值得推荐。",
    "第一次买这个品牌，{pos_detail}，超出预期。",
    "朋友推荐的，{pos_detail}，果然没让我失望。",
    "包装精美，{pos_detail}，五星好评。",
    "{pos_detail}，续航也很给力，整体很满意。",
    "这个价位能有这样的品质，{pos_detail}，必须好评。",
]

POSITIVE_DETAILS = [
    "运行流畅", "响应速度快", "操作简单", "颜值很高",
    "手感舒适", "音质清晰", "画质出色", "噪音小",
    "安装方便", "客服态度好", "物流很快", "质量过硬",
    "功能齐全", "设计人性化", "省电节能",
]

# 负向评论模板
NEGATIVE_TEMPLATES = [
    "价格太贵了，{neg_detail}，不值这个价。",
    "{neg_detail}，客服回复也很慢，差评。",
    "bug 太多了，{neg_detail}，体验很差。",
    "续航差，{neg_detail}，失望。",
    "收到就有问题，{neg_detail}，要求退货。",
    "等了好久才发货，{neg_detail}，不想再买了。",
    "{neg_detail}，做工也很粗糙，踩雷了。",
    "跟描述不符，{neg_detail}，很失望。",
    "用了一天就出问题，{neg_detail}，质量堪忧。",
    "噪音太大，{neg_detail}，影响使用。",
]

NEGATIVE_DETAILS = [
    "经常卡顿", "频繁闪退", "发热严重", "充电慢",
    "信号差", "屏幕漏光", "按键松动", "异味大",
    "配件缺失", "说明书不清楚", "连接不稳定", "耗电快",
    "画面模糊", "声音失真", "操作复杂",
]

# 中性评论模板
NEUTRAL_TEMPLATES = [
    "整体一般吧，{neu_detail}，中规中矩。",
    "还可以，{neu_detail}，不算惊艳但也能用。",
    "符合预期，{neu_detail}，没什么惊喜。",
    "凑合用，{neu_detail}，对得起这个价格。",
    "{neu_detail}，其他方面普普通通。",
    "马马虎虎，{neu_detail}，能接受。",
    "不功不过，{neu_detail}，就那样吧。",
    "基本满足需求，{neu_detail}，没有特别突出的地方。",
]

NEUTRAL_DETAILS = [
    "功能够用", "外观一般", "速度还行", "质量中等",
    "体验普通", "没什么特色", "表现平平", "有待提升",
    "不算好也不算差", "将就着用",
]


def generate_username() -> str:
    """生成随机用户名"""
    prefixes = ["小", "大", "老", "快乐的", "认真的", "爱买的", "普通的", "热心的", "低调的", "暴躁的"]
    suffixes = ["用户", "买家", "消费者", "网友", "小白", "达人", "粉丝", "路人", "吃瓜群众", "测评君"]
    return random.choice(prefixes) + random.choice(suffixes)


def generate_review_date() -> str:
    """生成随机日期（近一年内）"""
    days_ago = random.randint(0, 365)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d %H:%M:%S")


def generate_content(sentiment: str) -> str:
    """根据情感类型生成评论内容"""
    if sentiment == "positive":
        template = random.choice(POSITIVE_TEMPLATES)
        return template.format(pos_detail=random.choice(POSITIVE_DETAILS))
    elif sentiment == "negative":
        template = random.choice(NEGATIVE_TEMPLATES)
        return template.format(neg_detail=random.choice(NEGATIVE_DETAILS))
    else:
        template = random.choice(NEUTRAL_TEMPLATES)
        return template.format(neu_detail=random.choice(NEUTRAL_DETAILS))


def generate_sample_data(count: int = 100) -> List[Dict[str, str]]:
    """生成模拟评论数据"""
    reviews = []

    # 分配情感比例：正向 50%，负向 30%，中性 20%
    sentiments = (
        ["positive"] * 50
        + ["negative"] * 30
        + ["neutral"] * 20
    )
    random.shuffle(sentiments)

    for i in range(count):
        sentiment = sentiments[i]
        rating_map = {
            "positive": random.choice([4, 4, 4, 5, 5]),
            "negative": random.choice([1, 1, 2, 2, 3]),
            "neutral": random.choice([3, 3, 3, 4]),
        }

        reviews.append({
            "review_id": f"R{i + 1:04d}",
            "username": generate_username(),
            "rating": str(rating_map[sentiment]),
            "content": generate_content(sentiment),
            "created_at": generate_review_date(),
        })

    return reviews


def save_to_csv(reviews: List[Dict[str, str]], path: Path) -> None:
    """保存到 CSV"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["review_id", "username", "rating", "content", "created_at"])
        writer.writeheader()
        writer.writerows(reviews)


def main():
    """生成并保存模拟数据"""
    output = Path("data/raw_reviews.csv")
    reviews = generate_sample_data(100)
    save_to_csv(reviews, output)
    print(f"已生成 {len(reviews)} 条模拟评论 -> {output}")


if __name__ == "__main__":
    main()
