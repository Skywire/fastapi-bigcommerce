from bigcommerce.api import BigcommerceApi
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates

from app.config import config


def verify_jwt(jwt: str):
    user_data = BigcommerceApi.oauth_verify_payload(jwt, config['CLIENT_SECRET'])
    if user_data is False:
        raise HTTPException(401, {"error": "Invalid JWT token"})

    return user_data


async def verified_payload(signed_payload: str = None):
    return verify_jwt(signed_payload)


async def verified_bearer_header(jwt: str = Depends(HTTPBearer())):
    return verify_jwt(jwt.credentials)


async def jinja_templates():
    return Jinja2Templates(directory="app/view/templates")
