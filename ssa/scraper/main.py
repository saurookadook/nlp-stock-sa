from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.news_spider import NewsSpider
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# def sentiment_analyzer(item):
#     analyzer = SentimentIntensityAnalyzer()
#     text = item['content']
#     scores = analyzer.polarity_scores(text)
#     print(scores)


def post_process(items):
    clean_items = [...]  # post-process
    print("LOADING TO DB")


#   load_to_db(clean_items)


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(NewsSpider).addCallback(post_process)
    process.start()


if __name__ == "__main__":
    main()
