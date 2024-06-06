from utils.pydantic_helpers import SerializerArrowType


class TimestampsMixin:
    created_at: SerializerArrowType
    updated_at: SerializerArrowType
