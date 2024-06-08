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

    ARTICLE_DATA = "ArticleDataDB"
    REDDIT_DATA = "RedditDataDB"

    @staticmethod
    def db_type_name() -> Literal["source_discriminators"]:
        return "source_discriminators"


ONE_DAY_IN_SECONDS = 60 * 60 * 24
