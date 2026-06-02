"""评论爬虫模块"""

import csv
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests


class SteamReviewCrawler:
    """爬取 Steam 游戏评论"""

    API_URL = "https://store.steampowered.com/appreviews/{app_id}"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def crawl(self, app_id: str, max_reviews: int = 100, language: str = "schinese") -> List[Dict[str, Any]]:
        """
        爬取 Steam 评论。

        Args:
            app_id: Steam 游戏 ID（如 730 = CS2）
            max_reviews: 最多爬取条数
            language: 语言，schinese=简体中文
        """
        print(f"正在爬取 Steam 评论: app_id={app_id}, 语言={language}, 目标={max_reviews} 条")

        reviews = []
        cursor = "*"
        page = 0

        while len(reviews) < max_reviews:
            page += 1
            params = {
                "json": "1",
                "language": language,
                "filter": "recent",
                "num_per_page": "100",
                "cursor": cursor,
                "purchase_type": "all",
            }

            try:
                response = self.session.get(
                    self.API_URL.format(app_id=app_id),
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                print(f"  请求失败 (第{page}页): {e}")
                break
            except ValueError:
                print(f"  JSON 解析失败 (第{page}页)")
                break

            if data.get("success") != 1:
                print(f"  API 返回失败: {data}")
                break

            batch = data.get("reviews", [])
            if not batch:
                print(f"  没有更多评论")
                break

            for r in batch:
                if len(reviews) >= max_reviews:
                    break
                reviews.append(self._parse_review(r, app_id))

            cursor = data.get("cursor", "")
            print(f"  第{page}页: 获取 {len(batch)} 条, 累计 {len(reviews)} 条")

            if not cursor:
                break

            # 请求间隔 1-2 秒
            time.sleep(random.uniform(1.0, 2.0))

        print(f"爬取完成: 共 {len(reviews)} 条评论")
        return reviews

    def _parse_review(self, raw: Dict[str, Any], app_id: str) -> Dict[str, Any]:
        """解析单条 Steam 评论"""
        voted_up = raw.get("voted_up", True)
        timestamp = raw.get("timestamp_created", 0)

        # 清洗 content：替换换行符，去除逗号
        content = raw.get("review", "")
        content = content.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        content = content.replace(",", "，")  # 英文逗号替换为中文逗号，避免 CSV 问题

        return {
            "review_id": raw.get("recommendationid", ""),
            "username": raw.get("author", {}).get("steamid", "anonymous"),
            "rating": 5 if voted_up else 1,
            "content": content,
            "created_at": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "",
            "source": "steam",
            "voted_up": str(voted_up),
            "votes_up": raw.get("votes_up", 0),
            "app_id": app_id,
        }

    def save(self, reviews: List[Dict[str, Any]], path: Path) -> None:
        """保存评论到 CSV（utf-8-sig 编码）"""
        if not reviews:
            print("没有评论可保存")
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["review_id", "username", "rating", "content", "created_at", "source", "voted_up", "votes_up", "app_id"]

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reviews)

        print(f"已保存 -> {path} ({len(reviews)} 条)")


def crawl_steam_reviews(app_id: str, max_reviews: int = 100, language: str = "schinese") -> List[Dict[str, Any]]:
    """
    爬取 Steam 游戏评论的独立入口函数。

    Args:
        app_id: Steam 游戏 ID（如 730 = CS2）
        max_reviews: 最多爬取条数
        language: 语言，schinese=简体中文

    Returns:
        评论列表
    """
    crawler = SteamReviewCrawler()
    return crawler.crawl(app_id, max_reviews=max_reviews, language=language)
