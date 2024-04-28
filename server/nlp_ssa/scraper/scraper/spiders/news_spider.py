import json
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
from rich import inspect
from sqlalchemy import select

from nlp_ssa.db import db_session
from nlp_ssa.models.article_data import ArticleDataFacade
from nlp_ssa.models.stock import StockDB
from scraper.items import ScraperItem

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


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
        news_links = self._get_non_ad_links_from_response(response)

        for link in news_links:
            yield scrapy_splash.SplashRequest(
                url=link,
                callback=self.parse,
                cb_kwargs=dict(stock_slug=stock_slug),
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

    def parse(self, response, stock_slug):
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

        item = ScraperItem()
        item["Sentence"] = cleaned_text
        item["GroupId"] = source_group_id
        try:
            self.article_data_facade.create_or_update(
                payload=dict(
                    id=uuid.uuid4(),
                    quote_stock_symbol=stock_slug,
                    source_group_id=source_group_id,
                    source_url=response.url,
                    raw_content=raw_text,
                    sentence_tokens=cleaned_text,
                )
            )
            db_session.commit()
        except Exception as e:
            print(e, file=sys.stderr)
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

    def _debug_logger(
        self, *, header_text: str, variables: list = [], width: int = 200
    ):
        print(f" {header_text} ".center(width, "="))
        for var in variables:
            print(var)
        if not variables:
            print("=" * width)

    def _get_non_ad_links_from_response(self, response):
        stream_links = response.css("div.news-stream a::attr(href)").getall()
        # inspect(stream_links)

        news_links = []
        for link in stream_links:
            if link.startswith("/"):
                news_links.append(self.base_url + link)
            elif "finance.yahoo.com" in link:
                news_links.append(link)

        # inspect(news_links)
        return news_links
