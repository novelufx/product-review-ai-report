"""AI 报告生成模块 - 使用 Anthropic Claude API"""

import csv
import json
import os
import random
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv(override=True)

# 抽样配置
SAMPLE_CONFIG = {
    "positive": 25,
    "neutral": 20,
    "negative": 35,
}


class AIReportGenerator:
    """调用 Claude 生成产品口碑分析报告"""

    def generate(self) -> Dict[str, Any]:
        """读取数据，调用 AI 生成报告"""
        reviews = self._read_csv(Path("data/cleaned_reviews.csv"))
        analysis = self._read_json(Path("data/analysis_result.json"))

        # 抽样
        sampled = self._sample_reviews(reviews)

        # 尝试调用 AI
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                return self._call_ai(sampled, analysis)
            except Exception as e:
                print(f"AI 调用失败，使用本地模板: {e}")
                return self._fallback_report(sampled, analysis)
        else:
            print("未检测到 API Key，使用本地 fallback 模板")
            return self._fallback_report(sampled, analysis)

    def _read_csv(self, path: Path) -> List[Dict[str, str]]:
        """读取 CSV"""
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _read_json(self, path: Path) -> Dict[str, Any]:
        """读取 JSON"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _sample_reviews(self, reviews: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """按情感分层抽样，最多 80 条"""
        positive = [r for r in reviews if int(float(r["rating"])) >= 4]
        neutral = [r for r in reviews if int(float(r["rating"])) == 3]
        negative = [r for r in reviews if int(float(r["rating"])) <= 2]

        sampled = []
        sampled.extend(random.sample(positive, min(SAMPLE_CONFIG["positive"], len(positive))))
        sampled.extend(random.sample(neutral, min(SAMPLE_CONFIG["neutral"], len(neutral))))
        sampled.extend(random.sample(negative, min(SAMPLE_CONFIG["negative"], len(negative))))

        random.shuffle(sampled)
        return sampled

    def _call_ai(self, reviews: List[Dict[str, str]], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """调用 Anthropic Claude API"""
        from anthropic import Anthropic

        client = Anthropic()

        # 构建评论文本
        review_lines = []
        for r in reviews:
            rating = int(float(r["rating"]))
            sentiment = "正向" if rating >= 4 else ("中性" if rating == 3 else "负向")
            review_lines.append(f"[{sentiment}] 评分:{rating} - {r['content']}")
        reviews_text = "\n".join(review_lines)

        prompt = f"""你是一名资深产品经理和用户研究专家。

我会给你一批产品用户评论，以及基础统计数据。

请你完成以下任务：
1. 总结产品整体口碑。
2. 提炼用户最认可的优点。
3. 提炼用户最集中的痛点。
4. 分析用户背后的真实需求。
5. 给出具体产品改进建议。
6. 给出营销与运营建议。

要求：
- 不要空泛。
- 每个痛点必须引用或概括用户评论作为依据。
- 改进建议要有优先级。
- 输出必须是严格 JSON。
- 不要输出 Markdown。

## 评论数据（共 {len(reviews)} 条抽样）

{reviews_text}

## 整体统计

- 总评论数: {analysis['total_reviews']}
- 平均评分: {analysis['average_rating']}
- 评分分布: {json.dumps(analysis['rating_distribution'], ensure_ascii=False)}
- 情感分布: {json.dumps(analysis['sentiment_counts'], ensure_ascii=False)}
- 高频关键词: {', '.join(k['word'] for k in analysis['keywords'][:10])}

## JSON Schema

{{
  "summary": "一句话总结整体口碑",
  "positive_points": ["优点1", "优点2"],
  "pain_points": [
    {{
      "title": "痛点标题",
      "description": "详细描述",
      "evidence": "引用或概括用户评论",
      "severity": "high/medium/low"
    }}
  ],
  "user_needs": ["需求1", "需求2"],
  "improvement_suggestions": [
    {{
      "title": "建议标题",
      "reason": "原因说明",
      "priority": "high/medium/low"
    }}
  ],
  "marketing_suggestions": ["营销建议1", "营销建议2"]
}}"""

        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )

        # 提取 text 内容（跳过 thinking 块）
        content = ""
        for block in response.content:
            if block.type == "text":
                content = block.text
                break

        # 提取 JSON 块
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        result = json.loads(content.strip())
        return result

    def _fallback_report(self, reviews: List[Dict[str, str]], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """本地 fallback 模板，无 API 时使用"""
        negative = [r for r in reviews if int(float(r["rating"])) <= 2]
        positive = [r for r in reviews if int(float(r["rating"])) >= 4]

        # 提取常见痛点关键词
        pain_keywords = []
        for r in negative:
            pain_keywords.append(r["content"][:30])

        return {
            "summary": f"共 {analysis['total_reviews']} 条评论，平均评分 {analysis['average_rating']}，整体口碑{'良好' if analysis['average_rating'] >= 3.5 else '一般'}。",
            "positive_points": [
                "产品质量获得多数用户认可",
                "性价比受到好评",
            ],
            "pain_points": [
                {
                    "title": "质量问题",
                    "description": "部分用户反馈产品存在质量缺陷",
                    "evidence": pain_keywords[0] if pain_keywords else "暂无",
                    "severity": "high",
                },
                {
                    "title": "售后服务",
                    "description": "客服响应速度有待提升",
                    "evidence": pain_keywords[1] if len(pain_keywords) > 1 else "暂无",
                    "severity": "medium",
                },
            ],
            "user_needs": [
                "更稳定的产品质量",
                "更快的售后响应",
                "更详细的产品说明",
            ],
            "improvement_suggestions": [
                {
                    "title": "加强品控",
                    "reason": "减少用户投诉，提升复购率",
                    "priority": "high",
                },
                {
                    "title": "优化客服流程",
                    "reason": "提升用户满意度",
                    "priority": "medium",
                },
            ],
            "marketing_suggestions": [
                "突出性价比优势进行推广",
                "邀请满意用户进行口碑传播",
            ],
        }

    def save(self, report: Dict[str, Any], path: Path) -> None:
        """保存报告为 JSON"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
