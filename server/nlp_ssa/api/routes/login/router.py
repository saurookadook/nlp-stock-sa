# TODO: make these routes work :]
from fastapi import APIRouter, Depends, Request
from fastapi_csrf_protect import CsrfProtect


router = APIRouter()


@router.get("/login")
async def read_login():
    return {"message": "YOU GOTTA LOGIN, SON"}


@router.post("/login")
async def attempt_login(
    fast_api_request: Request = None, csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(fast_api_request)
    return {"message": "YOU GOTTA LOGIN, SON"}
