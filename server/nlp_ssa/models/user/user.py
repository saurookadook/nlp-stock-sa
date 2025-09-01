from pydantic import ConfigDict
from uuid import UUID

from utils.pydantic_helpers import BaseAppModel


class User(BaseAppModel):
    id: UUID
    username: str
    email: str
    # password: str
    first_name: str
    last_name: str
