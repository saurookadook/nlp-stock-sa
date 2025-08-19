import arrow
import json
import logging
import nltk
import re
import scrapy
import scrapy_splash
import sys
import uuid
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from pathlib import Path
from pprint import pprint as prettyprint
from rich import inspect
from sqlalchemy import select

from nlp_ssa.config.logging import ExtendedLogger
from nlp_ssa.db import db_session
from nlp_ssa.models.article_data import ArticleDataFacade, ArticleDataDB
from nlp_ssa.models.stock import StockDB
from nlp_ssa.models.sentiment_analysis import SentimentAnalysisDB
from scraper.items import ScraperItem
from scraper.spiders.base_spider import BaseSpider

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

logger: ExtendedLogger = logging.getLogger(__file__)


# -------------------------| WIP |-------------------------
class CNBCNewsSpider(BaseSpider):
    name = "news"
    base_url = "https://www.cnbc.com/"

    def start_requests(self):
        logger.info(f"  CNBCNewsSpider : start_requests  ".center(160, "!"))
        # stock_symbol_slugs = db_session.execute(
        #     select(StockDB.quote_stock_symbol)
        # ).all()

        # self.stock_slugs.extend([result[0] for result in stock_symbol_slugs])
        self.stock_slugs = ["TSLA"]

        url_configs = [
            dict(url=f"{self.base_url}/quotes/{slug}", stock_slug=slug)
            for slug in self.stock_slugs
        ]
        inspect(url_configs)

        for config in url_configs:
            yield scrapy_splash.SplashRequest(
                url=config["url"],
                callback=self.follow_quote_news_links,
                cb_kwargs=dict(stock_slug=config["stock_slug"]),
            )

    def follow_quote_news_links(self, response, stock_slug):
        news_item_configs = self._get_non_ad_non_pro_news_items_from_response(response)

        self._debug_logger(
            header_text="news_item_configs", variables=[news_item_configs]
        )
        for item_config in news_item_configs[0:1]:
            self._debug_logger(header_text="item_config", variables=[item_config])
            yield scrapy_splash.SplashRequest(
                url=item_config["url"],
                callback=self.parse,
                cb_kwargs=dict(
                    source_url=item_config["url"],
                    stock_slug=stock_slug,
                    thumbnail_url=item_config["thumbnail_url"],
                ),
                args={
                    "wait": 4,
                    # set rendering arguments here
                    "html": 1,
                    "png": 1,
                    # 'url' is prefilled from request url
                    # 'http_method' is set to 'POST' for POST requests
                    # 'body' is set to request body for POST requests
                },
                # optional parameters
                # "endpoint": "render.json",  # optional; default is render.html
                # "splash_url": "<url>",  # optional; overrides SPLASH_URL
                # "slot_policy": scrapy_splash.SlotPolicy.PER_DOMAIN,
                # "splash_headers": {},  # optional; a dict with headers sent to Splash
                # "dont_process_response": True,  # optional, default is False
                # "dont_send_headers": True,  # optional, default is False
                # "magic_response": False,  # optional, default is True
            )

    def parse(self, response, source_url, stock_slug, thumbnail_url):
        """
        - parse html
        - runs methods to pre-process data for nlp models
        - yields item
        """
        self._debug_logger(
            header_text="NewsSpider.parse",
            variables=[source_url, response.url, stock_slug],
        )

        article_content = response.css("div[id*=ArticleBody] div.group").get()
        if not article_content:
            raise Exception("NOPETOWN FOR CNBC :[")
        else:
            inspect(article_content)

    def _get_non_ad_non_pro_news_items_from_response(self, response):
        news_items = response.css(".LatestNews-item")

        news_item_configs = []
        for item in news_items:
            item_link = item.css("a::attr(href)").get()
            if item_link is None or item_link.startswith("/pro"):
                logger.warning(
                    f" WARNING: Skipping item: {item} - is either undefined or is 'Pro' article"
                )
                continue

            item_thumbnail = item.css("img::attr(src)").get()
            # self._debug_logger(
            #     header_text="news_item", variables=[item, item_link, item_thumbnail]
            # )
            # logger.debug(f"item_link: '{item_link}'")
            # logger.debug(f"item_thumbnail: '{item_thumbnail}'")
            if item_link.startswith("/"):
                news_item_configs.append(
                    dict(url=self.base_url + item_link, thumbnail_url=item_thumbnail)
                )
            elif "cnbc.com" in item_link:
                news_item_configs.append(
                    dict(url=item_link, thumbnail_url=item_thumbnail)
                )

        return news_item_configs
