import json
import nltk
import re
import scrapy
import scrapy_splash
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
from nlp_ssa.models.stock import StockDB
from scraper.items import ScraperItem

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


class NewsSpider(scrapy.Spider):
    name = "news"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "DOWNLOAD_DELAY": 2,
    }
    stock_slugs = []
    base_url = "https://finance.yahoo.com"

    def preprocess(self, documents):
        """
        Preprocesses a list of text documents by cleaning each one.
        """
        preprocessed_docs = []
        for doc in documents:
            preprocessed_docs.append(self.clean(doc))
        return preprocessed_docs

    def clean(self, text):
        """
        Cleans text by:
        - Removing URLs
        - Converting text to lowercase
        - Removing punctuation
        - Removing stopwords
        - Lemmatizing words
        """
        tokenizer = PunktSentenceTokenizer()
        lemmatizer = WordNetLemmatizer()

        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = text.lower()  # Convert to lowercase
        text = re.sub(r"[^a-zA-Z0-9]", " ", text)  # Remove punctuation

        text = tokenizer.tokenize(text)
        stops = set(stopwords.words("english"))
        text = [word for word in text if word not in stops]  # Remove stopwords
        text = [lemmatizer.lemmatize(word=word_1) for word_1 in text]  # Lemmatize
        return text

    def start_requests(self):
        stock_symbol_slugs = db_session.execute(
            select(StockDB.quote_stock_symbol)
        ).all()

        self.stock_slugs.extend([result[0] for result in stock_symbol_slugs])

        urls = [
            f"https://finance.yahoo.com/quote/{slug}/news" for slug in self.stock_slugs
        ]
        # urls.extend(
        #     [
        #         f"https://finance.yahoo.com/quote/{slug}/news"
        #         for slug in self.stock_slugs
        #     ]
        # )
        inspect(urls)

        for url in urls:
            yield scrapy_splash.SplashRequest(
                url=url, callback=self.follow_quote_news_links
            )

    def follow_quote_news_links(self, response):
        news_links = response.css("div.news-stream a::attr(href)").getall()
        inspect(news_links)
        news_links = [
            self.base_url + link if "finance.yahoo.com" not in link else link
            for link in news_links
        ]
        inspect(news_links)

        for link in news_links:
            yield scrapy_splash.SplashRequest(
                url=link,
                callback=self.parse,
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

    def parse(self, response):
        """
        - parse html
        - runs methods to pre-process data for nlp models
        - yields item
        """
        self._debug_logger(header_text="NewsSpider.parse")
        soup = BeautifulSoup(response.body, "html.parser")
        cleaned_text = self.clean(soup.get_text())
        item = ScraperItem()
        self._debug_logger(
            header_text="NewsSpider.parse - cleaned_text",
            variables=[cleaned_text],
            width=200,
        )
        item["Sentence"] = cleaned_text
        item["GroupId"] = uuid.uuid4()
        yield item

    def _debug_logger(
        self, *, header_text: str, variables: list = [], width: int = 200
    ):
        print(f" {header_text} ".center(width, "="))
        for var in variables:
            print(var)
        if not variables:
            print("=" * width)
