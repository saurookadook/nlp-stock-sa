from pydantic import BaseModel, ConfigDict
from typing import Any, Union
from uuid import UUID

# from models.article_data import ArticleData
from models.mixins import TimestampsMixin, SourceAssociationDB


class Source(BaseModel, TimestampsMixin):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data: Any  # ArticleData
