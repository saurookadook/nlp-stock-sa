from pydantic import BaseModel, ConfigDict
from uuid import UUID

from models.mixins import TimestampsMixin


class AnalysisView(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_group_id: UUID
    # owner_id: UUID
    user_id: UUID
