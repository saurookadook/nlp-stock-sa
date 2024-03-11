from enum import Enum


class SentimentEnum(Enum):

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


from models.sentiment_analysis.db import SentimentAnalysisDB
from models.sentiment_analysis.facade import SentimentAnalysisFacade
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.sentiment_analysis.sentiment_analysis import SentimentAnalysis
