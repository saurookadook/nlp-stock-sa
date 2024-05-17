from utils.pydantic_helpers import BaseResponseModel


class LoginResponse(BaseResponseModel):
    github_url: str
