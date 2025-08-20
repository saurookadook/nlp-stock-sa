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

logger: ExtendedLogger = logging.getLogger(__file__)


class NewsSpider(BaseSpider):
    name = "news"
    base_url = "https://finance.yahoo.com"

    def start_requests(self):
        # all_article_data = select(ArticleDataDB).where(ArticleDataDB.title == "")

        # for ad in db_session.scalars(all_article_data):
        #     yield scrapy_splash.SplashRequest(
        #         url=ad.source_url,
        #         callback=self.update_metadata_from_page,
        #         cb_kwargs=dict(current_ad=ad, stock_slug=ad.quote_stock_symbol),
        #     )

        stock_symbol_slugs = db_session.execute(
            select(StockDB.quote_stock_symbol)
        ).all()

        self.stock_slugs.extend([result[0] for result in stock_symbol_slugs])

        url_configs = [
            dict(url=f"https://finance.yahoo.com/quote/{slug}/news", stock_slug=slug)
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

        article_content = response.css("div.morpheusGridBody div.caas-body").get()
        if not article_content:
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
        item["Sentence"] = cleaned_text
        item["GroupId"] = source_group_id

        yield item

    # NOTE: can potentially remove this
    def update_metadata_from_page(self, response, current_ad, stock_slug):
        article_content = response.css("div.morpheusGridBody div.caas-body").get()
        if not article_content:
            return

        metadata = self._get_article_metadata(response)

        try:
            article_data_record = self.article_data_facade.create_or_update(
                payload=dict(
                    id=current_ad.id,
                    quote_stock_symbol=stock_slug,
                    source_url=response.url,
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
                    title=metadata["title"],
                )
            )
            db_session.commit()
        except Exception as e:
            logger.error(e, file=sys.stderr)

        item = ScraperItem()
        # item["ArticleData"] = str(current_ad.id)
        self._debug_logger(
            header_text="NewsSpider.update_metadata_from_page",
            variables=[f"{key}: {metadata[key]} " for key in metadata.keys()],
            width=240,
        )

        yield item

    def _get_non_ad_news_items_from_response(self, response):
        news_items = response.css("div.news-stream .stream-item")

        news_item_configs = []
        for item in news_items:
            item_link = item.css("a::attr(href)").get()
            if (
                item_link is None
                or not item_link.startswith("/")
                or "finance.yahoo.com" not in item_link
            ):
                logger.warning(f" WARNING: Skipping item: {item} ")
                continue

            trimmed_link = self._trim_query_params(item_link)
            item_url = (
                self.base_url + trimmed_link
                if trimmed_link.startswith("/")
                else trimmed_link
            )
            item_thumbnail = item.css("img::attr(src)").get()
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
            byline_wrapper = response.css('[class*="byline-wrapper"]')
            if byline_wrapper:
                metadata_dict["author"] = byline_wrapper.css(
                    '[class*="item-author"] *::text'
                ).get(default="")
                metadata_dict["last_updated_date"] = byline_wrapper.css(
                    "time::attr(datetime)"
                ).get(default="")
                metadata_dict["published_date"] = byline_wrapper.css(
                    "time::attr(datetime)"
                ).get(default="")

            metadata_dict["title"] = response.css(
                'meta[property="og:title"]::attr(content)'
            ).get(default="")
        except Exception as e:
            self._debug_logger(header_text="Error getting metadata", variables=[e])

        return metadata_dict
