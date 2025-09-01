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


class AuthProviderEnum(ExtendedEnum):

    APPLE = "apple"
    GITHUB = "github"
    GOOGLE = "google"
    MICROSOFT = "microsoft"

    @staticmethod
    def db_type_name() -> Literal["auth_providers"]:
        return "auth_providers"

    @classmethod
    def get_default(cls):
        return cls.GITHUB


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

    ArticleDataDB = "article_data"
    RedditDataDB = "reddit_data"

    @staticmethod
    def db_type_name() -> Literal["source_discriminators"]:
        return "source_discriminators"

    @classmethod
    def get_default(cls):
        return cls.ArticleDataDB


class TokenTypeEnum(ExtendedEnum):

    ACCESS = "access"  # Not sure if this is a real token type...?
    BEARER = "bearer"

    @staticmethod
    def db_type_name() -> Literal["token_types"]:
        return "token_types"

    @classmethod
    def get_default(cls):
        return cls.BEARER


ONE_DAY_IN_SECONDS = 60 * 60 * 24
EIGHT_HOURS_IN_SECONDS = 28800
SIX_MONTHS_IN_SECONDS = 15897600
