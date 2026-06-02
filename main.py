"""Product Review AI Report - 主入口"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="产品评论 AI 分析报告生成器")
    parser.add_argument("--url", type=str, help="产品页面 URL")
    parser.add_argument("--input", type=str, help="输入 CSV 文件路径")
    parser.add_argument("--output", type=str, default="reports", help="输出目录")
    parser.add_argument("--skip-crawl", action="store_true", help="跳过爬取步骤")
    parser.add_argument("--skip-clean", action="store_true", help="跳过清洗步骤")
    parser.add_argument("--sample", action="store_true", help="生成 100 条模拟评论数据")
    parser.add_argument("--clean", action="store_true", help="仅执行数据清洗")
    parser.add_argument("--analyze", action="store_true", help="仅执行情感分析")
    parser.add_argument("--ai", action="store_true", help="仅生成 AI 报告")
    parser.add_argument("--charts", action="store_true", help="仅生成图表")
    parser.add_argument("--report", action="store_true", help="生成最终 HTML 报告到 docs/")
    parser.add_argument("--all", action="store_true", help="运行完整流程")
    parser.add_argument("--crawl-steam", type=str, metavar="APP_ID", help="爬取 Steam 游戏评论（如 730）")
    parser.add_argument("--max-reviews", type=int, default=100, help="最大爬取条数（默认 100）")
    parser.add_argument("--language", type=str, default="schinese", help="评论语言（默认 schinese）")
    args = parser.parse_args()

    data_dir = Path("data")

    # 爬取 Steam 评论
    if args.crawl_steam:
        from src.crawler import crawl_steam_reviews, SteamReviewCrawler
        reviews = crawl_steam_reviews(args.crawl_steam, max_reviews=args.max_reviews, language=args.language)
        SteamReviewCrawler().save(reviews, data_dir / "raw_reviews.csv")
        print(f"\n下一步: python main.py --clean")
        return

    # 生成模拟数据（不需要第三方依赖）
    if args.sample:
        from src.sample_data import generate_sample_data, save_to_csv
        reviews = generate_sample_data(100)
        save_to_csv(reviews, data_dir / "raw_reviews.csv")
        print(f"已生成 {len(reviews)} 条模拟评论 -> data/raw_reviews.csv")
        return

    # 仅执行清洗
    if args.clean:
        from src.cleaner import ReviewCleaner
        input_file = args.input or str(data_dir / "raw_reviews.csv")
        cleaner = ReviewCleaner()
        cleaned, stats = cleaner.clean(input_file)
        cleaner.save(cleaned, data_dir / "cleaned_reviews.csv")
        print(f"清洗前: {stats['raw_count']} 条")
        print(f"清洗后: {stats['cleaned_count']} 条")
        print(f"已保存 -> data/cleaned_reviews.csv")
        return

    # 仅执行分析
    if args.analyze:
        from src.analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(str(data_dir / "cleaned_reviews.csv"))
        analyzer.save(result, data_dir / "analysis_result.json")
        print(f"评论总数: {result['total_reviews']}")
        print(f"平均评分: {result['average_rating']}")
        print(f"情感分布: {result['sentiment_counts']}")
        print(f"已保存 -> data/analysis_result.json")
        return

    # 仅生成 AI 报告
    if args.ai:
        from src.ai_report import AIReportGenerator
        ai_gen = AIReportGenerator()
        report = ai_gen.generate()
        ai_gen.save(report, data_dir / "ai_report.json")
        print(f"总结: {report['summary']}")
        print(f"痛点数: {len(report['pain_points'])}")
        print(f"已保存 -> data/ai_report.json")
        return

    # 仅生成图表
    if args.charts:
        from src.chart_generator import ChartGenerator
        output_dir = Path(args.output)
        chart_gen = ChartGenerator()
        fragments = chart_gen.generate_all(data_dir / "analysis_result.json", output_dir)
        for name, html in fragments.items():
            print(f"  {name}_chart.html ({len(html)} bytes)")
        print(f"已保存 -> {output_dir}/")
        return

    # 生成最终 HTML 报告
    if args.report:
        from src.report_generator import ReportGenerator
        docs_dir = Path("docs")
        report_gen = ReportGenerator()
        report_gen.generate(data_dir, docs_dir)
        print(f"报告已生成 -> docs/index.html")
        return

    # 运行完整流程
    if args.all:
        raw_path = data_dir / "raw_reviews.csv"
        cleaned_path = data_dir / "cleaned_reviews.csv"
        analysis_path = data_dir / "analysis_result.json"
        ai_path = data_dir / "ai_report.json"

        # Step 1: 模拟数据
        if not raw_path.exists():
            from src.sample_data import generate_sample_data, save_to_csv
            reviews = generate_sample_data(100)
            save_to_csv(reviews, raw_path)
            print(f"[1/6] 模拟数据已生成: {len(reviews)} 条 -> data/raw_reviews.csv")
        else:
            print(f"[1/6] 跳过: data/raw_reviews.csv 已存在")

        # Step 2: 清洗
        from src.cleaner import ReviewCleaner
        cleaner = ReviewCleaner()
        cleaned, stats = cleaner.clean(str(raw_path))
        cleaner.save(cleaned, cleaned_path)
        print(f"[2/6] 清洗完成: {stats['raw_count']} -> {stats['cleaned_count']} 条 -> data/cleaned_reviews.csv")

        # Step 3: 分析
        from src.analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(str(cleaned_path))
        analyzer.save(result, analysis_path)
        print(f"[3/6] 分析完成: 评分 {result['average_rating']}, 情感 {result['sentiment_counts']} -> data/analysis_result.json")

        # Step 4: AI 报告
        from src.ai_report import AIReportGenerator
        ai_gen = AIReportGenerator()
        report = ai_gen.generate()
        ai_gen.save(report, ai_path)
        print(f"[4/6] AI 报告完成: {len(report.get('pain_points', []))} 个痛点 -> data/ai_report.json")

        # Step 5: 图表
        from src.chart_generator import ChartGenerator
        chart_gen = ChartGenerator()
        docs_dir = Path("docs")
        fragments = chart_gen.generate_all(analysis_path, docs_dir)
        print(f"[5/6] 图表完成: {', '.join(f'{n}({len(h)}B)' for n, h in fragments.items())} -> docs/")

        # Step 6: 最终报告
        from src.report_generator import ReportGenerator
        report_gen = ReportGenerator()
        report_gen.generate(data_dir, docs_dir)
        print(f"[6/6] 报告完成 -> docs/index.html")
        print("\n全流程完成!")
        return

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: 爬取评论
    if not args.skip_crawl:
        if not args.url:
            print("错误: 需要 --url 参数")
            sys.exit(1)
        from src.crawler import ReviewCrawler
        crawler = ReviewCrawler()
        raw_reviews = crawler.crawl(args.url)
        crawler.save(raw_reviews, data_dir / "raw_reviews.csv")
        print(f"爬取完成: {len(raw_reviews)} 条评论")

    # Step 2: 清洗评论
    if not args.skip_clean:
        input_file = args.input or str(data_dir / "raw_reviews.csv")
        from src.cleaner import ReviewCleaner
        cleaner = ReviewCleaner()
        cleaned, stats = cleaner.clean(input_file)
        cleaner.save(cleaned, data_dir / "cleaned_reviews.csv")
        print(f"清洗完成: {stats['raw_count']} -> {stats['cleaned_count']} 条评论")

    # Step 3: 情感分析
    from src.analyzer import SentimentAnalyzer
    analyzer = SentimentAnalyzer()
    analyzed = analyzer.analyze(str(data_dir / "cleaned_reviews.csv"))
    print(f"分析完成: {len(analyzed)} 条评论")

    # Step 4: AI 报告
    from src.ai_report import AIReportGenerator
    ai_gen = AIReportGenerator()
    report_data = ai_gen.generate()
    ai_gen.save(report_data, data_dir / "ai_report.json")
    print("AI 报告生成完成")

    # Step 5: 生成图表
    from src.chart_generator import ChartGenerator
    chart_gen = ChartGenerator()
    fragments = chart_gen.generate_all(data_dir / "analysis_result.json", output_dir)
    print("图表生成完成")

    # Step 6: 生成 HTML 报告
    from src.report_generator import ReportGenerator
    report_gen = ReportGenerator()
    report_gen.generate(report_data, output_dir)
    print(f"报告已保存到 {output_dir}")


if __name__ == "__main__":
    main()
