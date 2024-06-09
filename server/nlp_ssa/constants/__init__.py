from enum import Enum
from typing import Literal


class SentimentEnum(Enum):

    COMPOUND = "compound"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"

    @staticmethod
    def db_type_name() -> Literal["sentiments"]:
        return "sentiments"


class SourceDiscriminatorEnum(Enum):

    # ARTICLE_DATA = "ArticleDataDB"
    # REDDIT_DATA = "RedditDataDB"
    ArticleDataDB = "article_data"
    RedditDataDB = "reddit_data"

    @staticmethod
    def db_type_name() -> Literal["source_discriminators"]:
        return "source_discriminators"

    @classmethod
    def get_default(cls):
        return cls.ArticleDataDB

    @classmethod
    def get_default_value(cls):
        return cls.get_default().value

    @classmethod
    def get_by_value(cls, value):
        for member in cls:
            if member.value == value:
                return member

        return None


ONE_DAY_IN_SECONDS = 60 * 60 * 24
