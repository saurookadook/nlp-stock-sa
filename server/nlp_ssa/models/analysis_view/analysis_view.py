from uuid import UUID

from models.mixins import TimestampsMixin
from utils.pydantic_helpers import BaseAppModel


class AnalysisView(BaseAppModel, TimestampsMixin):
    id: UUID
    source_group_id: UUID
    # owner_id: UUID
    user_id: UUID
