from pydantic import Field, field_validator
from typing import Annotated, Optional

from utils.pydantic_helpers import SerializerArrowType, generic_validator_with_default


# TODO: is there a way to do this without causing circular imports...?
# class OwnedByPolymorphicSourceMixin:
#     from models.source import Source

#     polymorphic_source: Annotated[Optional[Source], Field(default_factory=lambda: None)]

#     @field_validator("polymorphic_source")
#     @classmethod
#     def handle_field_default(cls, value, info):
#         return generic_validator_with_default(cls, value, info)


class TimestampsMixin:
    created_at: SerializerArrowType
    updated_at: SerializerArrowType
