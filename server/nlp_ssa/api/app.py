import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

from api.routes.api.analysis_views import router as api_analysis_views
from api.routes.api.article_data import router as api_article_data
from api.routes.api.stocks import router as api_stocks
from api.routes.api.users import router as api_users
from api.routes.login import router as login
from config import configure_logging, env_config


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


@app.get("/api/health-check")
async def read_health_check():
    # return JSONResponse(status_code=200, content={"message": "Hello, world!"})
    return {"message": "Yaaaaaay, health! Salud!"}


app.include_router(api_analysis_views.router)
app.include_router(api_article_data.router)
app.include_router(api_stocks.router)
app.include_router(api_users.router)
app.include_router(login.router)
