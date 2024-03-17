from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from utils.pydantic_helpers import ArrowType


class AnalysisView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_group_id: UUID
    owner_id: UUID
    user_id: Optional[UUID]
    created_at: ArrowType
    updated_at: ArrowType
