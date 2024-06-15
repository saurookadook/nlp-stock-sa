from enum import Enum
from typing import Literal


class ExtendedEnum(Enum):
    @classmethod
    def get_default_value(cls):
        """Inheriting classes must implement a `get_default` method"""
        return cls.get_default().value

    @classmethod
    def get_by_value(cls, value):
        for member in cls:
            if member.value == value:
                return member

        return None


class SentimentEnum(ExtendedEnum):

    COMPOUND = "compound"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"

    @staticmethod
    def db_type_name() -> Literal["sentiments"]:
        return "sentiments"

    @classmethod
    def get_default(cls):
        return cls.NEUTRAL


class SourceDiscriminatorEnum(ExtendedEnum):

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


ONE_DAY_IN_SECONDS = 60 * 60 * 24
