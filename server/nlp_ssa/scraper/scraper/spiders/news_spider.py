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

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

logger: ExtendedLogger = logging.getLogger(__file__)


class NewsSpider(scrapy.Spider):
    name = "news"
    article_data_facade = ArticleDataFacade(db_session=db_session)
    base_url = "https://finance.yahoo.com"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "DOWNLOAD_DELAY": 2,
    }
    stock_slugs = []
    lemmatizer = WordNetLemmatizer()
    tokenizer = PunktSentenceTokenizer()

    def preprocess(self, documents):
        """
        Preprocesses a list of text documents by cleaning each one.
        """
        preprocessed_docs = []
        for doc in documents:
            preprocessed_docs.append(self.clean(doc))
        return preprocessed_docs

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
                    "wait": 2,
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

        soup = BeautifulSoup(article_content, "html.parser")
        raw_text = soup.get_text()
        cleaned_text = self.clean(raw_text)
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
            logger.error(e, file=sys.stderr)

        item = ScraperItem()
        item["Sentence"] = cleaned_text
        item["GroupId"] = source_group_id

        yield item

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

    def clean(self, text):
        """
        Cleans text by:
        - Removing URLs
        - Converting text to lowercase
        - Removing punctuation
        - Removing stopwords
        - Lemmatizing words
        """
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = text.lower()  # Convert to lowercase
        text = re.sub(r"[^a-zA-Z0-9]", " ", text)  # Remove punctuation

        text = self.tokenizer.tokenize(text)
        stops = set(stopwords.words("english"))
        text = [word for word in text if word not in stops]  # Remove stopwords
        text = [self.lemmatizer.lemmatize(word=word_1) for word_1 in text]  # Lemmatize
        return text

    def _get_non_ad_news_items_from_response(self, response):
        news_items = response.css("div.news-stream .stream-item")

        news_item_configs = []
        for item in news_items:
            item_link = item.css("a::attr(href)").get()
            if item_link is None:
                logger.warning(f" WARNING: Skipping item: {item} ")
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
            elif "finance.yahoo.com" in item_link:
                news_item_configs.append(
                    dict(url=item_link, thumbnail_url=item_thumbnail)
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

    def _debug_logger(
        self, *, header_text: str, variables: list = [], width: int = 200
    ):
        print(f" {header_text} ".center(width, "="))
        for var in variables:
            prettyprint(var, indent=4, width=width, sort_dicts=True)
        if len(variables) > 0:
            print("=" * width)
