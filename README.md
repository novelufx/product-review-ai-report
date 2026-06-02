# Product Review AI Report

产品评论 AI 分析报告生成器 - 爬取评论、分析情感、生成可视化报告。

## 功能

- 爬取产品页面用户评论
- 清洗和预处理评论数据
- 关键词统计和情感分类
- AI 生成核心痛点和改进建议
- pyecharts 生成交互式图表
- Jinja2 生成静态 HTML 报告
- 支持 GitHub Pages 发布

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 OpenAI API Key

# 3. 运行
python main.py --url "https://example.com/product"
```

## 命令行参数

```bash
python main.py [OPTIONS]

Options:
  --url URL          产品页面 URL
  --input FILE       输入 CSV 文件路径 (跳过爬取)
  --output DIR       输出目录 (默认: reports)
  --skip-crawl       跳过爬取步骤
  --skip-clean       跳过清洗步骤
```

## 目录结构

```
product-review-ai-report/
├── data/              # 原始和清洗后的数据
├── docs/              # GitHub Pages 输出目录
├── reports/           # 生成的图表
├── src/               # 源代码
│   ├── crawler.py     # 评论爬虫
│   ├── cleaner.py     # 数据清洗
│   ├── analyzer.py    # 情感分析
│   ├── ai_report.py   # AI 报告生成
│   ├── chart_generator.py  # 图表生成
│   └── report_generator.py # HTML 报告生成
├── templates/         # Jinja2 模板
├── main.py            # 主入口
└── requirements.txt   # 依赖
```

## GitHub Pages 部署

1. 推送代码到 GitHub
2. 在仓库设置中启用 GitHub Pages
3. 选择 `docs/` 目录作为发布源
4. 访问 `https://username.github.io/product-review-ai-report/`
