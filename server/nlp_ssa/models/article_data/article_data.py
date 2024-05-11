from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional
from uuid import UUID

from utils.pydantic_helpers import SerializerArrowType


class ArticleData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str

    author: Optional[str] = ""
    last_updated_date: Optional[SerializerArrowType] = None
    # last_updated_date: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    published_date: Optional[SerializerArrowType] = None
    raw_content: Optional[str] = ""
    sentence_tokens: Optional[str] = ""
    title: Optional[str] = ""
    thumbnail_image_url: Optional[str] = ""
    created_at: SerializerArrowType
    # created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: SerializerArrowType
    # updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
