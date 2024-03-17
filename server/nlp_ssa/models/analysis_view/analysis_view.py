from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import WrapValidator
from typing import Annotated, Optional
from uuid import UUID

from utils.pydantic_helpers import convert_to_arrow_instance


class AnalysisView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_group_id: UUID
    owner_id: UUID
    user_id: Optional[UUID]
    created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
