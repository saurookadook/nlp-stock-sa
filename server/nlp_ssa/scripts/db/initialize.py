import os
from alembic import command, config

import db
from db import Base, engine

# from models import analysis_view, sentiment_analysis, stock, user
from models.article_data.db import ArticleDataDB
from models.analysis_view.db import AnalysisViewDB
from models.sentiment_analysis.db import SentimentAnalysisDB
from models.stock.db import StockDB
from models.user.db import UserDB


def initialize_database():
    """Initializes database, including creating tables and setting latest alembic revision"""
    Base.metadata.create_all(engine)
    alembic_ini = os.path.join(
        os.path.abspath(os.path.dirname(db.__file__) + "/../.."), "alembic.ini"
    )
    alembic_config = config.Config(alembic_ini)
    command.stamp(alembic_config, "head")


if __name__ == "__main__":
    initialize_database()
