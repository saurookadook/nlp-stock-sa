import arrow
import json
import logging
import nltk
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

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

logger: ExtendedLogger = logging.getLogger(__file__)


class CNBCNewsSpider(BaseSpider):
    """Spider for CNBC News (cnbc.com)

    -------------------------| WIP |-------------------------

    NOTES:
    - this site may need a subscription?
    """

    name = "news"
    base_url = "https://www.cnbc.com/"

    def start_requests(self):
        logger.info(f"  {self.__class__.__name__} : start_requests  ".center(160, "!"))
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
            header_text=f"{self.follow_quote_news_links.__qualname__} : news_item_configs for '{stock_slug}'",
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

        article_content_groups = response.css('[id*="ArticleBody"] > div.group')
        if not article_content_groups:
            logger.warning(
                f"NOPETOWN FOR '{source_url}' FROM CNBC :[ - No article content!!!"
            )

        article_content = []

        for el in article_content_groups:
            # inspect(el, methods=True, sort=True)

            if el.css("[class*=RelatedContent]"):
                continue

            article_content.append(el.get())

        # inspect(article_content)

        article_data_record = None
        source_group_id = uuid.uuid4()

        try:
            raw_text, cleaned_text = self.get_raw_and_cleaned_text(
                "\n".join(article_content)
            )
            metadata = self._get_article_metadata(response, source_url)

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
        item["record_id"] = (
            str(article_data_record.id) if article_data_record else "SKIPPED"
        )
        item["sentence"] = cleaned_text if cleaned_text is not None else ""
        item["source_group_id"] = source_group_id if source_group_id is not None else ""

        yield item

    def _get_article_metadata(self, response, source_url):
        metadata_dict = dict(
            author="",
            last_updated_date="",
            published_date="",
            title="",
        )

        try:
            article_header = response.css("[id*=ArticleHeader]")
            if not article_header:
                raise Exception(f"Can't find article header for '{source_url}'")

            author_wrapper = article_header.css("[class*=ArticleHeader-author]")
            if author_wrapper:
                metadata_dict["author"] = author_wrapper.css(
                    "[class*=authorName]::text"
                ).get(default="")

            timestamp_wrapper = article_header.css("[class*=ArticleHeader-time]")
            if timestamp_wrapper:
                metadata_dict["last_updated_date"] = timestamp_wrapper.css(
                    "time[itemprop=dateModified]::attr(datetime)"
                ).get(default="")
                metadata_dict["published_date"] = timestamp_wrapper.css(
                    "time[itemprop=datePublished]::attr(datetime)"
                ).get(default="")

            metadata_dict["title"] = article_header.css(
                'meta[property="og:title"]::attr(content)'
            ).get(default="")
        except Exception as e:
            self._debug_logger(header_text="Error getting metadata", variables=[e])

    def _get_non_ad_non_pro_news_items_from_response(self, response):
        news_items = response.css(".LatestNews-item")

        news_item_configs = []
        for item in news_items:
            item_link = item.css("a::attr(href)").get()
            if item_link is None or item_link.startswith("/pro"):
                logger.warning(
                    f"Skipping item - is either undefined or is 'Pro' article:\n {item}"
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
