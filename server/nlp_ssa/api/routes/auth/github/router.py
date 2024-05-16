import logging
import requests
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from urllib import parse

# TODO: remove
from rich import inspect
from config import env_vars


logger = logging.getLogger(__name__)
router = APIRouter()


def exchange_code(code):
    params = {
        "client_id": env_vars.GITHUB_OAUTH_CLIENT_ID,
        "client_secret": env_vars.GITHUB_OAUTH_CLIENT_SECRET,
        "code": code,
    }

    result = requests.post(
        env_vars.GITHUB_OAUTH_TOKEN_URL + parse.urlencode(params),
        headers={"Accept": "application/json"},
    )

    inspect(result, methods=True, sort=True)

    try:
        response = result.json()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nope :["
        )

    return response


@router.get("/github-callback")
async def github_oauth_callback(
    fast_api_request: Request = None,
    # token: str = Depends(oauth2_auth_code_scheme),
):
    inspect(fast_api_request, sort=True)
    inspect(fast_api_request.query_params, methods=True, sort=True)

    token_data = exchange_code(fast_api_request.query_params.get("code"))

    inspect(token_data)

    return RedirectResponse("https://nlp-ssa.dev/app")
