# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    Sentence = scrapy.Field()
    hrefs = scrapy.Field()
    GroupId = scrapy.Field()
    pass
