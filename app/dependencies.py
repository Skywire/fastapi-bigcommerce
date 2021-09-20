from bigcommerce.api import BigcommerceApi
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from app.config import config


async def verified_payload(signed_payload: str):
    user_data = BigcommerceApi.oauth_verify_payload(signed_payload, config['CLIENT_SECRET'])
    if user_data is False:
        raise HTTPException(401, {"error": "Invalid JWT token"})

    return user_data


async def jinja_templates():
    return Jinja2Templates(directory="app/view/templates")