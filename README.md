# Steam 评论口碑分析报告

这是我为了联系用户反馈分析和可视化报告搭配AI辅助总结功能做的一个小项目。

项目会从 Steam 公开评论接口获取游戏或软件的用户评论，对评论做清洗、统计和关键词分析，然后用大模型辅助总结用户反馈，最后生成一个静态网页报告。

## 项目背景

我在看 AI 产品实习岗位时发现，很多岗位都会要求做用户反馈整理、数据分析、竞品调研和产品改进建议。  
所以我想做一个比较完整的小项目，模拟产品同学如何从大量用户评论中提炼有价值的信息。

我选择 Steam 评论作为数据源，主要是因为它有公开评论接口，而且有「推荐 / 不推荐」字段，比较适合做口碑分析。

这个项目的重点不是爬虫本身，而是把用户评论转成一份能看的产品分析报告。

## 主要功能

目前项目支持：

- 根据 Steam AppID 获取公开评论
- 清洗评论数据，去除空评论和重复评论
- 将 Steam 的推荐 / 不推荐转换为简单评分和情绪标签
- 统计评论数量、平均评分、评分分布和情绪占比
- 使用 jieba 做中文分词，统计高频关键词
- 调用大模型辅助总结：
  - 用户认可的优点
  - 用户集中反馈的问题
  - 潜在需求
  - 产品改进建议
  - 运营建议
- 生成带图表的 HTML 报告
- 通过 GitHub Pages 发布报告页面

## 技术栈

- Python
- requests
- pandas
- jieba
- pyecharts
- Jinja2
- 大模型 API
- GitHub Pages

## 项目结构

```text
product-review-ai-report/
├── data/                 # 本地数据文件，不上传到 GitHub
├── docs/                 # GitHub Pages 发布目录
│   └── index.html
├── reports/              # 中间图表文件
├── src/
│   ├── crawler.py        # Steam 评论获取
│   ├── cleaner.py        # 数据清洗
│   ├── analyzer.py       # 评分、情绪、关键词分析
│   ├── ai_report.py      # 大模型总结
│   ├── chart_generator.py
│   └── report_generator.py
├── templates/
│   └── report_template.html
├── main.py
├── requirements.txt
└── README.md
