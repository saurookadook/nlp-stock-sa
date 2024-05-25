import logging
from fastapi import APIRouter, Depends, Request
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy import select

from api.routes.api.stocks.models import AllStocksResponse
from db import db_session


logger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/stocks/all", response_model=AllStocksResponse)
async def read_all_stocks():
    from models.stock import StockDB

    all_stocks = db_session.execute(select(StockDB).limit(100)).scalars().all()

    return {"data": all_stocks}


@router.post("/api/stocks/new")
async def create_stock_record(
    fast_api_request: Request = None, csrf_protect: CsrfProtect = Depends()
):
    # TODO: make this route work :]
    await csrf_protect.validate_csrf(fast_api_request)
    pass
