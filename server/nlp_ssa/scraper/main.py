#!/usr/bin/env python3

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.news_spider import NewsSpider
from scraper.spiders.bloomberg_spider import BloombergSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(NewsSpider)
    # process.crawl(BloombergSpider)
    process.start()


if __name__ == "__main__":
    main()
