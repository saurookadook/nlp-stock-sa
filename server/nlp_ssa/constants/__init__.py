from enum import Enum


class SentimentEnum(Enum):

    COMPOUND = "compound"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


class SourceDiscriminatorEnum(Enum):

    ARTICLE_DATA = "ArticleDataDB"
    REDDIT_DATA = "RedditDataDB"


ONE_DAY_IN_SECONDS = 60 * 60 * 24
