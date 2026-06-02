"""图表生成模块 (pyecharts)"""

from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

from pyecharts.charts import Pie, Bar, WordCloud
from pyecharts import options as opts


class ChartGenerator:
    """生成 pyecharts 图表"""

    def generate_sentiment_chart(self, reviews: List[Dict[str, Any]], output: Path) -> None:
        """生成情感分布饼图"""
        sentiments = Counter(r["sentiment"] for r in reviews)
        data = [list(item) for item in sentiments.items()]

        pie = (
            Pie()
            .add("", data)
            .set_global_opts(title_opts=opts.TitleOpts(title="情感分布"))
        )
        pie.render(str(output))

    def generate_keyword_chart(self, reviews: List[Dict[str, Any]], output: Path) -> None:
        """生成关键词词云"""
        words = []
        for r in reviews:
            words.extend(r.get("content", "").lower().split())

        stop_words = {"the", "a", "an", "is", "it", "to", "and", "of", "in", "for", "was"}
        filtered = [w for w in words if len(w) > 3 and w not in stop_words]
        word_counts = Counter(filtered).most_common(50)

        wc = (
            WordCloud()
            .add("", word_counts)
            .set_global_opts(title_opts=opts.TitleOpts(title="高频关键词"))
        )
        wc.render(str(output))

    def generate_rating_chart(self, reviews: List[Dict[str, Any]], output: Path) -> None:
        """生成评分分布柱状图"""
        ratings = Counter(int(r["rating"]) for r in reviews)
        x_data = sorted(ratings.keys())
        y_data = [ratings[x] for x in x_data]

        bar = (
            Bar()
            .add_xaxis([str(x) for x in x_data])
            .add_yaxis("评论数", y_data)
            .set_global_opts(title_opts=opts.TitleOpts(title="评分分布"))
        )
        bar.render(str(output))
