import arrow
import json
import logging
import scrapy_splash
import sys
import uuid
from pathlib import Path
from rich import inspect, pretty
from sqlalchemy import select

from nlp_ssa.config.logging import ExtendedLogger
from nlp_ssa.db import db_session
from nlp_ssa.models.article_data import ArticleDataFacade, ArticleDataDB
from nlp_ssa.models.stock import StockDB
from nlp_ssa.models.sentiment_analysis import SentimentAnalysisDB
from scraper.items import ScraperItem
from scraper.spiders.base_spider import BaseSpider

logger: ExtendedLogger = logging.getLogger("news_spider")


class YahooNewsSpider(BaseSpider):
    name: str = "news"
    base_url: str = "https://finance.yahoo.com"
    selectors: dict[str, str] = {
        "article_content": "div.morpheusGridBody div.caas-body, div.body-wrap div.body",
        "article_title": 'meta[property="og:title"]::attr(content)',
        "byline_wrapper": '.byline-attr, [class*="byline-wrapper"]',
        "byline_author": '[class*="byline-attr-author"]::text, [class*="item-author"] *::text',
        "byline_time": '[class*="byline-attr-time-"] time::attr(datetime), time::attr(datetime)',
        "item_link": "a::attr(href)",
        "item_thumbnail": "img::attr(src)",
        "news_items": "div.news-stream .stream-item",
    }

    def start_requests(self):
        stock_symbol_slugs = db_session.execute(
            select(StockDB.quote_stock_symbol)
        ).all()

        self.stock_slugs.extend([result[0] for result in stock_symbol_slugs])

        url_configs = [
            dict(url=f"{self.base_url}/quote/{slug}/news", stock_slug=slug)
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
        news_item_configs = self._get_non_ad_news_items_from_response(response)

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
            header_text="NewsSpider.parse", variables=[response.url, stock_slug]
        )

        article_content = response.css(self.selectors["article_content"]).get()
        if not article_content:
            self.logger.warning(
                f"UH OH! :o  ||  No article content found for '{response.url}'"
            )
            return

        raw_text, cleaned_text = self.get_cleaned_text(article_content)
        source_group_id = uuid.uuid4()

        self._debug_logger(
            header_text="NewsSpider.parse - cleaned_text",
            variables=[cleaned_text],
            width=200,
        )

        metadata = self._get_article_metadata(response)

        try:
            article_data_record = self.article_data_facade.create_or_update(
                payload=dict(
                    id=uuid.uuid4(),
                    quote_stock_symbol=stock_slug,
                    source_group_id=source_group_id,
                    source_url=response.url or source_url,
                    author=metadata["author"],
                    last_updated_date=(
                        ""
                        if not metadata["last_updated_date"]
                        else arrow.get(metadata["last_updated_date"]).to("utc")
                    ),
                    published_date=(
                        ""
                        if not metadata["published_date"]
                        else arrow.get(metadata["published_date"]).to("utc")
                    ),
                    raw_content=raw_text,
                    sentence_tokens=cleaned_text,
                    title=metadata["title"],
                    thumbnail_image_url=thumbnail_url,
                )
            )
            # logger.log_info_centered(" BEFORE COMMIT ")
            # inspect(article_data_record)

            db_session.commit()

            # logger.log_info_centered(" AFTER COMMIT ")
            # inspect(article_data_record)
        except Exception as e:
            self._handle_parse_method_exception(logger, source_url, e)

        item = ScraperItem()
        item["record_id"] = str(article_data_record.id)
        item["sentence"] = cleaned_text
        item["source_group_id"] = source_group_id

        yield item

    def _get_non_ad_news_items_from_response(self, response):
        news_items = response.css(self.selectors["news_items"])

        news_item_configs = []
        for item in news_items:
            item_link = item.css(self.selectors["item_link"]).get()
            if (
                item_link is None
                or not item_link.startswith("/")
                or "finance.yahoo.com" not in item_link
            ):
                logger.warning(f"Skipping item:\n{item}")
                continue

            trimmed_link = self._trim_query_params(item_link)
            item_url = (
                self.base_url + trimmed_link
                if trimmed_link.startswith("/")
                else trimmed_link
            )
            item_thumbnail = item.css(self.selectors["item_thumbnail"]).get()

            # self._debug_logger(
            #     header_text="news_item", variables=[item, item_link, item_thumbnail]
            # )
            # logger.debug(f"item_link: '{item_link}'")
            # logger.debug(f"item_thumbnail: '{item_thumbnail}'")
            news_item_configs.append(
                dict(
                    url=item_url,
                    thumbnail_url=item_thumbnail,
                )
            )

        return news_item_configs

    def _get_article_metadata(self, response):
        metadata_dict = dict(
            author="",
            last_updated_date="",
            published_date="",
            title="",
        )

        try:
            byline_wrapper = response.css(self.selectors["byline_wrapper"])
            if byline_wrapper:
                metadata_dict["author"] = byline_wrapper.css(
                    self.selectors["byline_author"]
                ).get(default="")
                metadata_dict["last_updated_date"] = byline_wrapper.css(
                    self.selectors["byline_time"]
                ).get(default="")
                metadata_dict["published_date"] = byline_wrapper.css(
                    self.selectors["byline_time"]
                ).get(default="")

            metadata_dict["title"] = response.css(self.selectors["article_title"]).get(
                default=""
            )
        except Exception as e:
            self._debug_logger(header_text="Error getting metadata", variables=[e])

        return metadata_dict
