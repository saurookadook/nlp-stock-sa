from uuid import UUID

from utils.pydantic_helpers import BaseAppModel


class AnalysisView(BaseAppModel):
    id: UUID
    source_group_id: UUID
    # owner_id: UUID
    user_id: UUID
