from typing import List

from models.sentiment_analysis import SentimentAnalysis
from utils.pydantic_helpers import BaseResponseModel


class SentimentAnalysisEntry(BaseResponseModel, SentimentAnalysis):
    pass


class SentimentAnalysesData(BaseResponseModel):
    quote_stock_symbol: str
    sentiment_analyses: List[SentimentAnalysisEntry]


class SentimentAnalysesBySlugResponse(BaseResponseModel):
    data: SentimentAnalysesData
