# TODO: make these routes work :]
import logging
from fastapi import APIRouter, Depends, Request
from fastapi_csrf_protect import CsrfProtect

from config import configure_logging
from db import db_session

configure_logging(app_name="nlp_ssa.api.routes.stocks")
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/stocks/new")
async def create_stock_record(
    fast_api_request: Request = None, csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(fast_api_request)
    pass
