from pydantic import BaseModel
from uuid import UUID

from utils.pydantic_helpers import ArrowType


class User(BaseModel):
    class Config:
        orm_mode = True

        id: UUID
        username: str
        # password: str
        first_name: str
        last_name: str
        created_at: ArrowType
        updated_at: ArrowType
