from utils.pydantic_helpers import BaseResponseModel


class LoginResponse(BaseResponseModel):
    apple_url: str = ""
    github_url: str = ""
    google_url: str = ""
    microsoft_url: str = ""
