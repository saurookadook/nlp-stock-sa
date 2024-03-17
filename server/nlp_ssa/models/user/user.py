from pydantic import BaseModel, ConfigDict
from uuid import UUID

from utils.pydantic_helpers import ArrowType


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    # password: str
    first_name: str
    last_name: str
    created_at: ArrowType
    updated_at: ArrowType
