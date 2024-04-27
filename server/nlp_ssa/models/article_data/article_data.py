from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import WrapValidator
from typing import Annotated, List
from uuid import UUID

from utils.pydantic_helpers import convert_to_arrow_instance


class ArticleData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    source_url: str
    raw_content: str = ""
    sentence_tokens: List[str] = []
    created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
