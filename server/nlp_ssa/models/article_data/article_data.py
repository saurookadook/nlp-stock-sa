from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated, Optional
from uuid import UUID

from models.mixins import TimestampsMixin
from models.source.source import Source
from utils.pydantic_helpers import SerializerArrowType, generic_validator_with_default


class ArticleData(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str
    data_source: Annotated[Optional[Source], Field(default_factory=lambda: None)]

    author: Annotated[Optional[str], Field(default_factory=lambda: "")]
    last_updated_date: Annotated[
        Optional[SerializerArrowType], Field(default_factory=lambda: None)
    ]
    published_date: Annotated[
        Optional[SerializerArrowType], Field(default_factory=lambda: None)
    ]
    raw_content: Annotated[Optional[str], Field(default_factory=lambda: "")]
    sentence_tokens: Annotated[Optional[str], Field(default_factory=lambda: "")]
    thumbnail_image_url: Annotated[Optional[str], Field(default_factory=lambda: "")]
    title: Annotated[Optional[str], Field(default_factory=lambda: "")]

    @field_validator(
        "author",
        "last_updated_date",
        "published_date",
        "raw_content",
        "sentence_tokens",
        "thumbnail_image_url",
        "title",
    )
    @classmethod
    def handle_field_defaults(cls, value, info):
        return generic_validator_with_default(cls, value, info)
