"""HTML 报告生成模块 (Jinja2)"""

from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    """生成 HTML 报告"""

    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, report_data: Dict[str, Any], output_dir: Path) -> None:
        """生成 HTML 报告"""
        template = self.env.get_template("report_template.html")
        html = template.render(**report_data)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "index.html"
        output_file.write_text(html, encoding="utf-8")
