from bigcommerce.api import BigcommerceApi
from fastapi.exceptions import HTTPException

from app.config import config


async def verified_payload(signed_payload: str):
    user_data = BigcommerceApi.oauth_verify_payload(signed_payload, config['CLIENT_SECRET'])
    if user_data is False:
        raise HTTPException(401, {"error": "Invalid JWT token"})

    return user_data