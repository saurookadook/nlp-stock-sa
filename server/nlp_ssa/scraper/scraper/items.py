# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    record_id = scrapy.Field()
    sentence = scrapy.Field()
    source_group_id = scrapy.Field()

    def __repr__(self):
        return "\n--".join(
            [
                "ScraperItem: ",
                f"record_id: {self['record_id']}",
                f"sentence: {self['sentence']}",
            ]
        )
