from typing import List, Optional
from uuid import UUID

from utils.pydantic_helpers import BaseResponseModel, SerializerArrowType


class ArticleDataEntry(BaseResponseModel):
    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str

    author: Optional[str] = ""
    last_updated_date: Optional[SerializerArrowType] = None
    published_date: Optional[SerializerArrowType] = None
    raw_content: Optional[str] = ""
    sentence_tokens: Optional[str] = ""
    title: Optional[str] = ""
    thumbnail_image_url: Optional[str] = ""
    created_at: SerializerArrowType
    updated_at: SerializerArrowType


class ArticleDataResponse(BaseResponseModel):
    data: List[ArticleDataEntry]
