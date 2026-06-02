"""AI 报告生成模块"""

import os
from typing import List, Dict, Any
from collections import Counter

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIReportGenerator:
    """使用 AI 生成分析报告"""

    def __init__(self):
        self.client = OpenAI()

    def generate(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成完整报告数据"""
        if not reviews:
            return self._empty_report()

        sentiments = Counter(r["sentiment"] for r in reviews)
        ratings = [r["rating"] for r in reviews]

        return {
            "summary": self._generate_summary(reviews),
            "sentiment_distribution": dict(sentiments),
            "average_rating": sum(ratings) / len(ratings) if ratings else 0,
            "total_reviews": len(reviews),
            "keywords": self._extract_keywords(reviews),
            "pain_points": self._generate_pain_points(reviews),
            "suggestions": self._generate_suggestions(reviews),
        }

    def _generate_summary(self, reviews: List[Dict[str, Any]]) -> str:
        """调用 AI 生成总结"""
        # 取样部分评论发送给 AI
        sample = reviews[:20]
        comments = "\n".join(f"- {r['content'][:100]}" for r in sample)

        prompt = f"""分析以下产品评论，用中文总结用户的核心反馈：

{comments}

请用 2-3 句话总结。"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI 总结生成失败: {e}"

    def _generate_pain_points(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """提取用户痛点"""
        negative = [r for r in reviews if r["sentiment"] == "negative"]
        if not negative:
            return ["暂无明显痛点"]

        comments = "\n".join(f"- {r['content'][:100]}" for r in negative[:10])
        prompt = f"""从以下负面评论中提取 3 个核心痛点，用中文列出：

{comments}

格式：每行一个痛点，简短描述。"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return response.choices[0].message.content.strip().split("\n")
        except Exception as e:
            return [f"痛点提取失败: {e}"]

    def _generate_suggestions(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """生成改进建议"""
        comments = "\n".join(f"- {r['content'][:100]}" for r in reviews[:15])
        prompt = f"""基于以下产品评论，给出 3 条产品改进建议，用中文回答：

{comments}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return response.choices[0].message.content.strip().split("\n")
        except Exception as e:
            return [f"建议生成失败: {e}"]

    def _extract_keywords(self, reviews: List[Dict[str, Any]], top_n: int = 10) -> List[str]:
        """提取高频关键词"""
        stop_words = {"the", "a", "an", "is", "it", "to", "and", "of", "in", "for", "was", "this", "with"}
        words = []
        for r in reviews:
            words.extend(w for w in r.get("content", "").lower().split() if len(w) > 3 and w not in stop_words)
        return [word for word, _ in Counter(words).most_common(top_n)]

    def _empty_report(self) -> Dict[str, Any]:
        """空报告"""
        return {
            "summary": "暂无评论数据",
            "sentiment_distribution": {},
            "average_rating": 0,
            "total_reviews": 0,
            "keywords": [],
            "pain_points": [],
            "suggestions": [],
        }
