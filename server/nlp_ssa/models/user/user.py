from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import WrapValidator
from typing import Annotated
from uuid import UUID

from utils.pydantic_helpers import convert_to_arrow_instance


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    # password: str
    first_name: str
    last_name: str
    created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
