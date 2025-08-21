import arrow
import json
import logging
import re
import scrapy_splash
import uuid
from rich import inspect, pretty

from nlp_ssa.config.logging import ExtendedLogger
from nlp_ssa.db import db_session
from nlp_ssa.models.article_data import ArticleDataFacade, ArticleDataDB
from nlp_ssa.models.stock import StockDB
from nlp_ssa.models.sentiment_analysis import SentimentAnalysisDB
from scraper.items import ScraperItem
from scraper.spiders.base_spider import BaseSpider

logger: ExtendedLogger = logging.getLogger(__file__)


class MarketWatchSpider(BaseSpider):
    """Spider for MarketWatch (marketwatch.com)

    NOTES:
    - it would seem this site needs a subscription
    - it may also be bouncing the crawlers based on some of the
        401 responses I've gotten
    """

    name = "news"
    base_url = "https://www.marketwatch.com"

    def start_requests(self):
        logger.info(f"  {self.__class__.__name__} : start_requests  ".center(160, "!"))
        # stock_symbol_slugs = db_session.execute(
        #     select(StockDB.quote_stock_symbol)
        # ).all()

        # self.stock_slugs.extend([result[0] for result in stock_symbol_slugs])
        self.stock_slugs = ["TSLA"]

        url_configs = [
            dict(url=self._build_request_url(slug), stock_slug=slug)
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
            header_text=f"{self.follow_quote_news_links.__qualname__} : news_item_configs",
            variables=[news_item_configs],
        )
        for item_config in news_item_configs:
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
            header_text=self.parse.__qualname__,
            variables=[source_url, response.url, stock_slug],
        )

        main_content = response.css("div#maincontent").get()
        if not main_content:
            logger.warning(
                f"NOPETOWN FOR '{source_url}' FROM MarketWatch :[ - No article content!!!"
            )

        inspect(main_content)

        raw_text, cleaned_text = self.get_cleaned_text(main_content)
        metadata = self._get_article_metadata(response)
        source_group_id = uuid.uuid4()

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

    def _build_request_url(self, slug):
        stock_type = "fund" if slug in self.fund_slugs else "stock"

        return f"{self.base_url}/investing/{stock_type}/{slug}"

    def _get_article_metadata(self, response):
        metadata_dict = dict(
            author="",
            last_updated_date="",
            published_date="",
            title="",
        )

        try:
            byline_wrapper = response.css("#maincontent .article__byline")
            if byline_wrapper:
                metadata_dict["author"] = byline_wrapper.css(
                    "a[class*=AuthorLink] *::text"
                ).get(default="")

            timestamp_wrapper = response.css("#maincontent .author__timestamp")
            if timestamp_wrapper:
                metadata_dict["last_updated_date"] = timestamp_wrapper.css(
                    ".last time::attr(datetime)"
                ).get(default="")
                metadata_dict["published_date"] = timestamp_wrapper.css(
                    ".first time::attr(datetime)"
                ).get(default="")

            metadata_dict["title"] = response.css(
                "#maincontent .article__headline *::text"
            ).get(default="")
        except Exception as e:
            self._debug_logger(header_text="Error getting metadata", variables=[e])

    def _get_non_ad_non_pro_news_items_from_response(self, response):
        base_area_selector = "#maincontent .region--primary .column--primary"
        news_items = response.css(
            f"{base_area_selector} .top--quote--headlines .element--article, "
            f"{base_area_selector} .more-headlines .element--article"
        )

        news_item_configs = []
        for item in news_items:
            guid = item.css("::attr(data-guid)").get()
            self._debug_logger(header_text="  guid  ", variables=[guid])

            item_link = item.css(
                ".article__content .article__headline a::attr(href)"
            ).get()
            if item_link is None or item_link.find("marketwatch.com") == -1:
                logger.warning(f"Skipping item:\n {item} ")
                continue

            item_thumbnail = item.css("figure img::attr(data-srcset)").get(default="")
            item_thumbnail_match = re.match(
                r"[^\s]+", item_thumbnail, flags=re.MULTILINE
            )

            trimmed_link = self._trim_query_params(item_link)
            item_url = (
                self.base_url + trimmed_link
                if item_link.startswith("/")
                else trimmed_link
            )
            item_thumbnail_url = (
                item_thumbnail_match.group(0)
                if item_thumbnail_match is not None
                else None
            )

            news_item_configs.append(
                dict(
                    url=item_url,
                    thumbnail_url=item_thumbnail_url,
                )
            )

        return news_item_configs
