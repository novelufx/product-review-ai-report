"""HTML 报告生成模块 (Jinja2)"""

import csv
import json
import random
from pathlib import Path
from typing import Dict, Any, List

from jinja2 import Environment, FileSystemLoader

from src.chart_generator import ChartGenerator


class ReportGenerator:
    """读取全部数据，生成最终 HTML 报告到 docs/index.html"""

    SENTIMENT_LABELS = {"positive": "正向", "neutral": "中性", "negative": "负向"}

    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_csv(self, path: Path, limit: int = 10) -> List[Dict[str, str]]:
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            return []
        random.shuffle(rows)
        return rows[:limit]

    def generate(self, data_dir: Path, output_dir: Path) -> None:
        """
        读取 data/ 下的 JSON + CSV，
        生成图表 HTML 片段，渲染最终报告到 output_dir/index.html。
        """
        analysis = self._load_json(data_dir / "analysis_result.json")
        ai_report = self._load_json(data_dir / "ai_report.json")
        sample_reviews = self._load_csv(data_dir / "cleaned_reviews.csv", limit=10)

        # 生成图表 HTML 片段
        chart_gen = ChartGenerator()
        output_dir.mkdir(parents=True, exist_ok=True)
        fragments = chart_gen.generate_all(data_dir / "analysis_result.json", output_dir)

        # 情感分布 key 转中文
        sentiment_display = {
            self.SENTIMENT_LABELS.get(k, k): v
            for k, v in analysis.get("sentiment_counts", {}).items()
        }

        template = self.env.get_template("report_template.html")
        html = template.render(
            total_reviews=analysis.get("total_reviews", 0),
            average_rating=analysis.get("average_rating", 0),
            rating_distribution=analysis.get("rating_distribution", {}),
            sentiment_counts=sentiment_display,
            keywords=analysis.get("keywords", []),
            summary=ai_report.get("summary", ""),
            positive_points=ai_report.get("positive_points", []),
            pain_points=ai_report.get("pain_points", []),
            user_needs=ai_report.get("user_needs", []),
            improvement_suggestions=ai_report.get("improvement_suggestions", []),
            marketing_suggestions=ai_report.get("marketing_suggestions", []),
            sample_reviews=sample_reviews,
            chart_sentiment=fragments.get("sentiment", ""),
            chart_rating=fragments.get("rating", ""),
            chart_keyword=fragments.get("keyword", ""),
        )

        output_file = output_dir / "index.html"
        output_file.write_text(html, encoding="utf-8")
