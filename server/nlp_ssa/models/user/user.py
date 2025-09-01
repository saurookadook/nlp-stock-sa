from pydantic import ConfigDict
from uuid import UUID

from models.mixins import TimestampsMixin
from utils.pydantic_helpers import BaseAppModel


class User(BaseAppModel, TimestampsMixin):
    id: UUID
    username: str
    email: str
    # password: str
    first_name: str
    last_name: str
