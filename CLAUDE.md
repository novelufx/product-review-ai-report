# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

产品评论 AI 分析报告生成器 - 爬取电商产品评论，进行情感分析，调用 AI 生成痛点和建议，最终输出可视化 HTML 报告。

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 完整流程运行
python main.py --url "https://example.com/product"

# 跳过爬取，使用已有数据
python main.py --skip-crawl

# 指定输入文件
python main.py --input data/raw_reviews.csv --skip-crawl
```

## 架构

数据处理流水线，main.py 串联 6 个步骤：

1. **crawler.py** - 爬取产品页面评论，输出 `data/raw_reviews.csv`
2. **cleaner.py** - 清洗文本（去 HTML、规范化），输出 `data/cleaned_reviews.csv`
3. **analyzer.py** - 基于词典的情感分析，返回 sentiment/score
4. **ai_report.py** - 调用 OpenAI API 生成总结、痛点、建议
5. **chart_generator.py** - pyecharts 生成 3 个图表（情感饼图、词云、评分柱状图）
6. **report_generator.py** - Jinja2 渲染模板，输出 `docs/index.html`

## 关键依赖

- `requests` + `beautifulsoup4`: 爬虫
- `pandas`: 数据处理（可选，当前用 csv 模块）
- `pyecharts`: 图表生成
- `jinja2`: HTML 模板渲染
- `openai`: AI 报告生成

## 配置

- `.env` 存放 `OPENAI_API_KEY`
- crawler.py 中的选择器需根据目标网站调整

## 输出目录

- `docs/` - GitHub Pages 发布目录，包含最终 `index.html`
- `reports/` - 中间图表文件
