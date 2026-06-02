"""图表生成模块 (pyecharts)"""

import json
from pathlib import Path
from typing import Dict, Any

from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType


class ChartGenerator:
    """从 analysis_result.json 读取数据，生成 pyecharts 图表"""

    # 中文情感标签映射
    SENTIMENT_LABELS = {"positive": "正向", "neutral": "中性", "negative": "负向"}
    SENTIMENT_COLORS = {"positive": "#52c41a", "neutral": "#faad14", "negative": "#f5222d"}

    def __init__(self, theme: ThemeType = ThemeType.MACARONS):
        self.theme = theme

    def load_data(self, json_path: Path) -> Dict[str, Any]:
        """读取 analysis_result.json"""
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_sentiment_chart(self, data: Dict[str, Any], output: Path) -> str:
        """
        生成情绪分布饼图。
        返回 HTML 片段。
        """
        sentiment_counts = data.get("sentiment_counts", {})
        pie_data = [
            [self.SENTIMENT_LABELS.get(k, k), v]
            for k, v in sentiment_counts.items()
        ]

        pie = (
            Pie(init_opts=opts.InitOpts(theme=self.theme, width="500px", height="350px"))
            .add(
                "",
                pie_data,
                radius=["40%", "70%"],
                label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="情绪分布", pos_left="center"),
                legend_opts=opts.LegendOpts(pos_bottom="0%"),
            )
            .set_colors([self.SENTIMENT_COLORS.get(k, "#999") for k in sentiment_counts.keys()])
        )

        output.parent.mkdir(parents=True, exist_ok=True)
        pie.render(str(output))
        return pie.render_embed()

    def generate_rating_chart(self, data: Dict[str, Any], output: Path) -> str:
        """
        生成评分分布柱状图。
        返回 HTML 片段。
        """
        rating_dist = data.get("rating_distribution", {})
        x_data = sorted(rating_dist.keys(), key=lambda x: int(x))
        y_data = [rating_dist[x] for x in x_data]

        bar = (
            Bar(init_opts=opts.InitOpts(theme=self.theme, width="500px", height="350px"))
            .add_xaxis([f"{x}星" for x in x_data])
            .add_yaxis("评论数", y_data, bar_width="40%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="评分分布", pos_left="center"),
                xaxis_opts=opts.AxisOpts(name="评分"),
                yaxis_opts=opts.AxisOpts(name="数量"),
            )
        )

        output.parent.mkdir(parents=True, exist_ok=True)
        bar.render(str(output))
        return bar.render_embed()

    def generate_keyword_chart(self, data: Dict[str, Any], output: Path, top_n: int = 15) -> str:
        """
        生成高频关键词柱状图。
        返回 HTML 片段。
        """
        keywords = data.get("keywords", [])[:top_n]
        x_data = [k["word"] for k in keywords]
        y_data = [k["count"] for k in keywords]

        bar = (
            Bar(init_opts=opts.InitOpts(theme=self.theme, width="700px", height="400px"))
            .add_xaxis(x_data)
            .add_yaxis("出现次数", y_data, bar_width="50%")
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="高频关键词 TOP15", pos_left="center"),
                xaxis_opts=opts.AxisOpts(name="次数"),
                yaxis_opts=opts.AxisOpts(name="关键词"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(position="right"),
            )
        )

        output.parent.mkdir(parents=True, exist_ok=True)
        bar.render(str(output))
        return bar.render_embed()

    def generate_all(self, json_path: Path, output_dir: Path) -> Dict[str, str]:
        """
        生成全部图表，返回 {chart_name: html_fragment} 字典。
        """
        data = self.load_data(json_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        fragments = {}
        fragments["sentiment"] = self.generate_sentiment_chart(data, output_dir / "sentiment_chart.html")
        fragments["rating"] = self.generate_rating_chart(data, output_dir / "rating_chart.html")
        fragments["keyword"] = self.generate_keyword_chart(data, output_dir / "keyword_chart.html")

        return fragments
