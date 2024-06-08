from pydantic import BaseModel, ConfigDict
from typing import Union
from uuid import UUID

from models.article_data import ArticleData
from models.mixins import TimestampsMixin


class Source(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data: Union[ArticleData]
