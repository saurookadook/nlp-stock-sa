from typing import List, Optional
from uuid import UUID

from utils.pydantic_helpers import BaseResponseModel, SerializerArrowType


class ArticleDataEntry(BaseResponseModel):
    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str
    raw_content: Optional[str] = ""
    sentence_tokens: Optional[List[str]] = []
    created_at: SerializerArrowType
    updated_at: SerializerArrowType


class ArticleDataResponse(BaseResponseModel):
    data: List[ArticleDataEntry]
