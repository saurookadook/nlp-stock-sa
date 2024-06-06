from pydantic import BaseModel

from utils.pydantic_helpers import SerializerArrowType


class TimestampsMixin(BaseModel):
    created_at: SerializerArrowType
    updated_at: SerializerArrowType
