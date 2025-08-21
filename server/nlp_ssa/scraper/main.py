#!/usr/bin/env python3
from rich import inspect, pretty
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.bloomberg_spider import BloombergSpider
from scraper.spiders.cnbc_spider import CNBCNewsSpider
from scraper.spiders.market_watch_spider import MarketWatchSpider
from scraper.spiders.yahoo_news_spider import YahooNewsSpider
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
    process = CrawlerProcess(get_project_settings())

    spiders = [
        # BloombergSpider,
        CNBCNewsSpider,
        MarketWatchSpider,
        # YahooNewsSpider,
    ]

    for spider in spiders:
        process.crawl(spider)
        # process.crawl(spider).addCallback(post_process)

    process.start()


if __name__ == "__main__":
    main()
