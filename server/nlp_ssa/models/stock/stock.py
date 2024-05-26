from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import WrapValidator
from typing import Annotated, Optional
from uuid import UUID

from utils.pydantic_helpers import convert_to_arrow_instance


class Stock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    full_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    exchange_name: Optional[str]
    created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
