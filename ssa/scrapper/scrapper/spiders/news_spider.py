from pathlib import Path
import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            "https://www.wsj.com/finance?mod=nav_top_section"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"scrapped-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")