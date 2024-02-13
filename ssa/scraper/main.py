from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.news_spider import NewsSpider

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(NewsSpider)
    # process.crawl(MySpider2)
    process.start()

if __name__ == "__main__":
    main()
