import nltk
import re
import scrapy
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from pathlib import Path
from pprint import pprint as prettyprint
from rich import inspect
from sqlalchemy import select

from nlp_ssa.db import db_session
from nlp_ssa.models.article_data import ArticleDataFacade, ArticleDataDB
from nlp_ssa.models.stock import StockDB
from nlp_ssa.models.sentiment_analysis import SentimentAnalysisDB

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


class BaseSpider(scrapy.Spider):
    article_data_facade: ArticleDataFacade = ArticleDataFacade(db_session=db_session)
    custom_settings: dict = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "DOWNLOAD_DELAY": 2,
    }
    stock_slugs: list[str] = []
    lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
    tokenizer: PunktSentenceTokenizer = PunktSentenceTokenizer()

    # TODO: need to add a 'type' column to `stocks` so we can
    # differentiate between stocks, funds, etc.
    fund_slugs: list[str] = ["IJR", "SCHD", "SPY", "SWPPX", "VOO", "VO", "VYM"]

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
        cleaned_text = re.sub(r"http\S+", "", text)  # Remove URLs
        cleaned_text = cleaned_text.lower()  # Convert to lowercase
        cleaned_text = re.sub(r"[^a-zA-Z0-9]", " ", cleaned_text)  # Remove punctuation

        cleaned_text = self.tokenizer.tokenize(cleaned_text)
        stops = set(stopwords.words("english"))
        cleaned_text = [
            word for word in cleaned_text if word not in stops
        ]  # Remove stopwords
        cleaned_text = [
            self.lemmatizer.lemmatize(word=word_1) for word_1 in cleaned_text
        ]  # Lemmatize
        return cleaned_text

    def get_raw_and_cleaned_text(self, content):
        soup = BeautifulSoup(content, "html.parser")
        raw_text = soup.get_text()
        return raw_text, self.clean(raw_text)

    def _trim_query_params(self, url_str):
        query_param_start_index = url_str.find("?")

        return (
            url_str[0:query_param_start_index]
            if query_param_start_index > -1
            else url_str
        )

    def _handle_parse_method_exception(self, logger, source_url, exception):
        logger.error(f"Caught exception while parsing '{source_url}':\n")
        logger.exception(exception)

    def _debug_logger(
        self, *, header_text: str, variables: list = [], width: int = 200
    ):
        print(f" {header_text} ".center(width, "="))
        for var in variables:
            prettyprint(var, indent=4, width=width, sort_dicts=True)
        if len(variables) > 0:
            print("=" * width)
