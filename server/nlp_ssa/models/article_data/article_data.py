from __future__ import annotations
from pydantic import Field, field_validator
from typing import Annotated, Optional
from uuid import UUID

from models.mixins import TimestampsMixin
from models.source import Source
from utils.pydantic_helpers import (
    BaseAppModel,
    SerializerArrowType,
    generic_cyclic_references_validator,
    generic_validator_with_default,
)


class ArticleData(
    # OwnedByPolymorphicSourceMixin,
    BaseAppModel,
    TimestampsMixin,
):
    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str
    polymorphic_source: Annotated[Source, Field(default_factory=lambda: None)]

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
        "polymorphic_source",
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

    @field_validator("polymorphic_source", mode="wrap")
    @classmethod
    def drop_cyclic_references_in_polymorphic_source(cls, data_value, validator_func):
        from models.source.db import SourceDB

        return generic_cyclic_references_validator(
            cls,
            data_value,
            validator_func,
            nested_classes=[SourceDB],
            nested_attr="data",
        )
