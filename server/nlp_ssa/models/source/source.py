from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated, Optional
from uuid import UUID

from constants import SourceDiscriminatorEnum
from models.mixins import TimestampsMixin
from utils.pydantic_helpers import SerializerArrowType, generic_validator_with_default


class Source(TimestampsMixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    data_type_id: Annotated[Optional[UUID], Field(default_factory=lambda: None)]
    data_type: Annotated[
        Optional[SourceDiscriminatorEnum], Field(default_factory=lambda: None)
    ]
    source_owner_name: Annotated[Optional[str], Field(default_factory=lambda: "")]

    @field_validator("data_type_id", "data_type", "source_owner_name")
    @classmethod
    def handle_field_defaults(cls, value, info):
        return generic_validator_with_default(cls, value, info)
