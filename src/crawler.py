"""评论爬虫模块"""

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class Review:
    """评论数据结构"""
    title: str
    content: str
    rating: float
    author: str
    date: str


class ReviewCrawler:
    """爬取产品评论"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def crawl(self, url: str) -> List[Review]:
        """从 URL 爬取评论"""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return self._parse_reviews(response.text)

    def _parse_reviews(self, html: str) -> List[Review]:
        """解析 HTML 中的评论"""
        soup = BeautifulSoup(html, "html.parser")
        reviews = []

        # TODO: 根据目标网站调整选择器
        for item in soup.select(".review-item"):
            review = Review(
                title=self._get_text(item, ".review-title"),
                content=self._get_text(item, ".review-content"),
                rating=self._get_rating(item, ".rating"),
                author=self._get_text(item, ".author"),
                date=self._get_text(item, ".date"),
            )
            reviews.append(review)

        return reviews

    def _get_text(self, element, selector: str) -> str:
        """获取元素文本"""
        el = element.select_one(selector)
        return el.get_text(strip=True) if el else ""

    def _get_rating(self, element, selector: str) -> float:
        """获取评分"""
        el = element.select_one(selector)
        if el:
            try:
                return float(el.get_text(strip=True))
            except ValueError:
                pass
        return 0.0

    def save(self, reviews: List[Review], path: Path) -> None:
        """保存评论到 CSV"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(Review.__dataclass_fields__.keys()))
            writer.writeheader()
            for review in reviews:
                writer.writerow(asdict(review))
