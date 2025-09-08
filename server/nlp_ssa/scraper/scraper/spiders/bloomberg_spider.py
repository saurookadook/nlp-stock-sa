from pathlib import Path
import uuid
import scrapy
from scraper.items import ScraperItem
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


class BloombergSpider(scrapy.Spider):
    name = "news"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "DOWNLOAD_DELAY": 2,
    }
    group_id = uuid.uuid4()

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
        urls = ["https://www.bloomberg.com/markets"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_bloomberg_sub_links(self, response):
        """
        - parse yahoo sub links only
        - runs methods to pre-process data for nlp models
        - yields item
        """
        links_to_include = ["https"]

        links = response.css("a::attr(href)").getall()
        for link in links:
            if (
                all(keyword in link for keyword in links_to_include)
                and "login" not in link
            ):
                yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        """
        - parse html
        - runs methods to pre-process data for nlp models
        - yields item
        """
        soup = BeautifulSoup(response.body, "html.parser")
        cleaned_text = self.clean(soup.get_text())
        item = ScraperItem()
        # item["record_id"] = str(article_data_record.id) if article_data_record else "SKIPPED"
        item["sentence"] = cleaned_text if cleaned_text is not None else ""
        item["source_group_id"] = self.group_id if self.group_id is not None else ""
        yield item
