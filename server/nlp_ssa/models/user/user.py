from pydantic import BaseModel, ConfigDict
from uuid import UUID

from models.mixins import TimestampsMixin


class User(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    # password: str
    first_name: str
    last_name: str
