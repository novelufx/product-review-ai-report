# Steam 游戏评论 AI 口碑分析报告

基于 Steam 游戏评论的 AI 智能分析工具 - 爬取评论、清洗数据、情感分析、AI 生成口碑报告、可视化图表。

## 功能

- 爬取 Steam 游戏评论（支持中文/英文）
- 清洗和预处理评论数据
- 关键词统计（jieba 分词）和情感分类
- AI 生成核心痛点和改进建议（支持 Anthropic Claude API）
- pyecharts 生成交互式图表
- Jinja2 生成静态 HTML 报告
- 支持 GitHub Pages 发布

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key（可选，不配置则使用本地 fallback 模板）
cp .env.example .env
# 编辑 .env 填入你的 Anthropic API Key

# 3. 爬取 Steam 评论
python main.py --crawl-steam 431960 --max-reviews 100

# 4. 运行完整流程
python main.py --all
```

## 命令行参数

```bash
python main.py [OPTIONS]

# 单步执行
python main.py --crawl-steam APP_ID  # 爬取 Steam 评论
python main.py --sample              # 生成模拟数据
python main.py --clean               # 清洗数据
python main.py --analyze             # 情感分析
python main.py --ai                  # AI 报告
python main.py --charts              # 生成图表
python main.py --report              # 生成 HTML 报告

# 完整流程
python main.py --all

# 可选参数
--max-reviews N    # 最大爬取条数（默认 100）
--language LANG    # 评论语言（默认 schinese）
--input FILE       # 输入 CSV 文件路径
--output DIR       # 输出目录（默认 reports）
```

## 常用 Steam 游戏 ID

| 游戏 | App ID |
|------|--------|
| Counter-Strike 2 | 730 |
| Wallpaper Engine | 431960 |
| Terraria | 105600 |
| Stardew Valley | 413150 |

## 目录结构

```
product-review-ai-report/
├── data/              # 原始和清洗后的数据（gitignore）
├── docs/              # GitHub Pages 输出目录
├── reports/           # 生成的图表（gitignore）
├── src/               # 源代码
│   ├── crawler.py     # Steam 评论爬虫
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
