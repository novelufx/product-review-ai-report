"""情感分析模块"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

import jieba


# 停用词表
STOP_WORDS = {
    "的", "了", "是", "我", "也", "很", "就", "都", "还", "一个", "这个",
    "在", "不", "有", "和", "人", "这", "中", "大", "为", "上", "个",
    "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
}


class SentimentAnalyzer:
    """评论情感分析"""

    def analyze(self, input_path: str) -> Dict[str, Any]:
        """
        分析 CSV 文件，返回完整分析结果。
        """
        reviews = self._read_csv(input_path)
        ratings = [int(float(r["rating"])) for r in reviews]

        # 评分分布
        rating_distribution = dict(sorted(Counter(ratings).items()))

        # 情感分类
        sentiments = [self._classify_sentiment(r) for r in ratings]
        sentiment_counts = dict(Counter(sentiments))

        # 关键词统计
        keywords = self._extract_keywords(reviews, top_n=20)

        result = {
            "total_reviews": len(reviews),
            "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
            "rating_distribution": rating_distribution,
            "sentiment_counts": sentiment_counts,
            "keywords": keywords,
        }

        return result

    def _read_csv(self, path: str) -> List[Dict[str, str]]:
        """读取 CSV"""
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _classify_sentiment(self, rating: int) -> str:
        """根据评分分类情感"""
        if rating >= 4:
            return "positive"
        elif rating == 3:
            return "neutral"
        else:
            return "negative"

    def _extract_keywords(self, reviews: List[Dict[str, str]], top_n: int = 20) -> List[Dict[str, Any]]:
        """使用 jieba 分词并统计高频关键词"""
        words = []
        for r in reviews:
            content = r.get("content", "")
            tokens = jieba.lcut(content)
            words.extend(w for w in tokens if len(w) > 1 and w not in STOP_WORDS)

        counter = Counter(words)
        return [{"word": word, "count": count} for word, count in counter.most_common(top_n)]

    def save(self, result: Dict[str, Any], path: Path) -> None:
        """保存分析结果为 JSON"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
