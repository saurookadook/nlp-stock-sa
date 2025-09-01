from __future__ import annotations
from pydantic import Field, field_validator
from typing import Annotated, Optional, Union
from uuid import UUID

from constants import SourceDiscriminatorEnum
from models.mixins import TimestampsMixin
from utils.pydantic_helpers import (
    BaseAppModel,
    generic_validator_with_default,
    generic_cyclic_references_validator,
)


class Source(BaseAppModel, TimestampsMixin):
    id: UUID
    data_type_id: Annotated[Optional[UUID], Field(default_factory=lambda: None)]
    data_type: Annotated[
        Optional[SourceDiscriminatorEnum], Field(default_factory=lambda: None)
    ]
    data: Optional[Union[ArticleData]] = Field(default_factory=lambda: None)
    source_owner_name: Annotated[Optional[str], Field(default_factory=lambda: "")]

    @field_validator("data_type_id", "data_type", "data", "source_owner_name")
    @classmethod
    def handle_field_defaults(cls, value, info):
        return generic_validator_with_default(cls, value, info)

    @field_validator("data", mode="wrap")
    @classmethod
    def drop_cyclic_references_in_data(cls, data_value, validator_func):
        from models.article_data.db import ArticleDataDB

        return generic_cyclic_references_validator(
            cls,
            data_value,
            validator_func,
            nested_classes=[ArticleDataDB],
            nested_attr="polymorphic_source",
        )
