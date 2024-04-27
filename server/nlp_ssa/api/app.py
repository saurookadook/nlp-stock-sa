import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from sqlalchemy import insert, select
from pydantic import BaseModel
from uuid import uuid4

from config import configure_logging, env_config
from db import db_session


configure_logging(app_name="nlp_ssa.api")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.warning("Shutting down nlpssa server-api...")


app = FastAPI(lifespan=lifespan)


class CsrfSettings(BaseModel):
    secret_key: str = env_config["csrf_secret"]
    csrf_header_name: str = "csrf-token"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=403, content={"detail": exc.message})


@app.get("/api/users/test")
async def read_users_test():
    from models.user import UserDB, UserFacade

    user_facade = UserFacade(db_session=db_session)

    try:
        logger.warning(f"{'='*40} getting user {'='*40}")
        user = user_facade.get_one_by_username(username="gordis-goobis")
    except UserFacade.NoResultFound:
        logger.warning(f"{'='*40} creating user {'='*40}")
        users = db_session.scalars(
            insert(UserDB).returning(UserDB),
            [
                {
                    "id": uuid4(),
                    "username": "gordis-goobis",
                    "first_name": "Gordo",
                    "last_name": "Ovalle-Maskiell",
                }
            ],
        )
        db_session.commit()
        user = users.first()

    return {"user": user}


@app.get("/api/analysis-views/test")
async def read_analysis_views():
    from models.analysis_view import AnalysisViewDB
    from models.user import UserFacade
    from models.sentiment_analysis import SentimentAnalysisDB

    user_facade = UserFacade(db_session=db_session)

    try:
        user = user_facade.get_one_by_username("ovalle15")
    except Exception as e:
        raise e

    analysis_views = (
        db_session.execute(
            select(AnalysisViewDB)
            .where(AnalysisViewDB.user_id == user.id)
            .order_by(AnalysisViewDB.source_group_id)
        )
        .scalars()
        .all()
    )

    source_group_ids = [av.source_group_id for av in analysis_views]
    sentiment_analyses = (
        db_session.execute(
            select(SentimentAnalysisDB)
            .where(SentimentAnalysisDB.source_group_id.in_(source_group_ids))
            .order_by(SentimentAnalysisDB.source_group_id)
        )
        .scalars()
        .all()
    )

    results = []

    for tuple_result in zip(analysis_views, sentiment_analyses):
        results.append(
            dict(analysis_view=tuple_result[0], sentiment_analysis=tuple_result[1])
        )

    return results


@app.get("/api/article-data/{stock_slug}")
async def read_article_data_by_slug(stock_slug: str):
    from models.article_data import ArticleDataDB

    article_data_rows = (
        db_session.execute(
            select(ArticleDataDB).where(
                ArticleDataDB.quote_stock_symbol == stock_slug.upper()
            )
        )
        .scalars()
        .all()
    )

    return [ad_data.__dict__ for ad_data in article_data_rows]


@app.get("/api/health-check")
async def read_health_check():
    # return JSONResponse(status_code=200, content={"message": "Hello, world!"})
    return {"message": "Yaaaaaay, health! Salud!"}


@app.get("/login")
async def read_login():
    return {"message": "YOU GOTTA LOGIN, SON"}


@app.get("/")
async def read_root():
    # return JSONResponse(status_code=200, content={"message": "Hello, world!"})
    return {"message": "Hello, world!"}
