from typing import List

from models.article_data import ArticleData
from utils.pydantic_helpers import BaseResponseModel


class ArticleDataEntry(BaseResponseModel, ArticleData):
    pass


class GroupedArticleData(BaseResponseModel):
    quote_stock_symbol: str
    article_data: List[ArticleDataEntry]


class ArticleDataResponse(BaseResponseModel):
    data: List[GroupedArticleData]
