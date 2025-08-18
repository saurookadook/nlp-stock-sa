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


class BaseSpider(scrapy.Spider):
    article_data_facade = ArticleDataFacade(db_session=db_session)
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

    def _debug_logger(
        self, *, header_text: str, variables: list = [], width: int = 200
    ):
        print(f" {header_text} ".center(width, "="))
        for var in variables:
            prettyprint(var, indent=4, width=width, sort_dicts=True)
        if len(variables) > 0:
            print("=" * width)
