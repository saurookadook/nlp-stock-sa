from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated, Optional
from uuid import UUID

from constants import SentimentEnum
from models.source import Source
from utils.pydantic_helpers import (
    BaseAppModel,
    generic_cyclic_references_validator,
    generic_validator_with_default,
)


class AnalysisOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    compound: float
    neg: float
    neu: float
    pos: float


class SentimentAnalysis(BaseAppModel):
    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_id: Annotated[Optional[UUID], Field(default_factory=lambda: None)]
    source: Annotated[Optional[Source], Field(default_factory=lambda: None)]
    output: AnalysisOutput
    score: float
    sentiment: SentimentEnum

    @field_validator("source_id", "source")
    @classmethod
    def handle_field_defaults(cls, value, info):
        return generic_validator_with_default(cls, value, info)

    @field_validator("source", mode="wrap")
    @classmethod
    def drop_cyclic_references_in_source(cls, data_value, validator_func):
        from models.source.db import SourceDB

        return generic_cyclic_references_validator(
            cls,
            data_value,
            validator_func,
            nested_classes=[SourceDB],
            nested_attr="data",
        )
