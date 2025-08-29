import logging
from fastapi import APIRouter, Depends, Request
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy import select

from api.routes.api.stocks.models import AllStocksResponse, SingularStockResponse
from config.logging import ExtendedLogger
from db import db_session


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/stocks/{stock_slug}", response_model=SingularStockResponse)
async def read_singular_stock_by_quote_stock_symbol(stock_slug: str):
    from models.stock import StockFacade

    singular_stock = None

    try:
        singular_stock = StockFacade(
            db_session=db_session
        ).get_one_by_quote_stock_symbol(quote_stock_symbol=stock_slug)
    except Exception as e:
        logger.error(e)

    # TODO: maybe get some other related data?

    return {"data": singular_stock}


@router.get("/api/stocks", response_model=AllStocksResponse)
async def read_all_stocks():
    from models.stock import StockDB, Stock

    all_stocks = db_session.execute(select(StockDB).limit(100)).scalars().all()

    return {"data": [Stock.model_validate(s) for s in all_stocks]}


@router.post("/api/stocks/new")
async def create_stock_record(
    fast_api_request: Request = None, csrf_protect: CsrfProtect = Depends()
):
    # TODO: make this route work :]
    await csrf_protect.validate_csrf(fast_api_request)
    pass
