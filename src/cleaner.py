"""数据清洗模块"""

import csv
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple


class ReviewCleaner:
    """清洗和标准化评论数据"""

    def clean(self, input_path: str) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """
        清洗 CSV 文件中的评论。

        返回: (清洗后的评论列表, 统计信息)
        """
        raw_reviews = self._read_csv(input_path)
        stats = {"raw_count": len(raw_reviews)}

        reviews = self._remove_empty_content(raw_reviews)
        reviews = self._remove_duplicate_content(reviews)
        reviews = [self._clean_review(r) for r in reviews]
        reviews = [r for r in reviews if r is not None]

        stats["cleaned_count"] = len(reviews)
        stats["removed_empty"] = stats["raw_count"] - len(self._remove_empty_content(raw_reviews))
        stats["removed_duplicate"] = len(self._remove_empty_content(raw_reviews)) - len(reviews) - stats.get("removed_invalid", 0)

        return reviews, stats

    def _read_csv(self, path: str) -> List[Dict[str, str]]:
        """读取 CSV（自动处理 BOM）"""
        with open(path, "r", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))

    def _remove_empty_content(self, reviews: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """删除 content 为空的行"""
        return [r for r in reviews if r.get("content", "").strip()]

    def _remove_duplicate_content(self, reviews: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """删除重复 content（保留第一条）"""
        seen = set()
        unique = []
        for r in reviews:
            content = r.get("content", "").strip()
            if content not in seen:
                seen.add(content)
                unique.append(r)
        return unique

    def _clean_review(self, review: Dict[str, str]) -> Dict[str, Any] | None:
        """清洗单条评论，返回 None 表示跳过"""
        content = self._clean_text(review.get("content", ""))
        if not content:
            return None

        rating = self._parse_rating(review.get("rating", "0"))
        if rating is None:
            return None

        return {
            "review_id": review.get("review_id", "").strip(),
            "username": review.get("username", "").strip(),
            "rating": rating,
            "content": content,
            "content_length": len(content),
            "created_at": review.get("created_at", "").strip(),
        }

    def _clean_text(self, text: str) -> str:
        """清洗文本：去除控制字符、多余空白"""
        # 去除控制字符（保留中文标点和换行）
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
        # 去除 HTML 标签
        text = re.sub(r"<[^>]+>", "", text)
        # 将换行符、制表符替换为空格
        text = re.sub(r"[\n\r\t]+", " ", text)
        # 合并多个空格
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _parse_rating(self, rating_str: str) -> int | None:
        """解析评分，确保是 1-5 的整数，无效返回 None"""
        try:
            rating = int(float(rating_str.strip()))
            if 1 <= rating <= 5:
                return rating
            return None
        except (ValueError, AttributeError):
            return None

    def save(self, reviews: List[Dict[str, Any]], path: Path) -> None:
        """保存清洗后的数据"""
        if not reviews:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
            writer.writeheader()
            writer.writerows(reviews)
