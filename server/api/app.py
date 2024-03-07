import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel


logger = logging.getLogger(__name__)

config = dict(csrf_secret="TMP")
logger.warning(f"{('='*40)} server.app::config {('='*40)}")
logger.warning(dir(config))


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.warning("Shutting down nlpssa server-api...")


app = FastAPI(lifespan=lifespan)


class CsrfSettings(BaseModel):
    secret_key: str = config["csrf_secret"]
    csrf_header_name: str = "csrf-token"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=403, content={"detail": exc.message})


@app.get("/api/health-check")
async def read_health_check():
    # return JSONResponse(status_code=200, content={"message": "Hello, world!"})
    return {"message": "Hello, world!"}


@app.get("/")
async def read_root():
    # return JSONResponse(status_code=200, content={"message": "Hello, world!"})
    return {"message": "Hello, world!"}
