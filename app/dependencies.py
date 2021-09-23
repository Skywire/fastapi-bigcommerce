from bigcommerce.api import BigcommerceApi
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from jwt import decode as jwt_decode

from app.config import config


async def verified_jwt(signed_payload_jwt: str = None):
    user_data = BigcommerceApi.oauth_verify_payload_jwt(signed_payload_jwt, config['CLIENT_SECRET'],
                                                        config['CLIENT_ID'])
    if user_data is False:
        raise HTTPException(401, {"error": "Invalid JWT token"})

    return user_data


async def verified_bearer_header(bearer: str = Depends(HTTPBearer())):
    # Haha BC signs admin JWTs and customer JWTs with different algorithms, what fun!
    # Try the HS256 supported by the official library first, if that fails do a raw PyJWT decode using HS512
    jwt = bearer.credentials
    try:
        user_data = BigcommerceApi.oauth_verify_payload_jwt(jwt, config['CLIENT_SECRET'], config['CLIENT_ID'])
        if user_data is False:
            raise HTTPException(401, {"error": "Invalid JWT token"})
    except:
        user_data = jwt_decode(jwt, config['CLIENT_SECRET'], algorithms=["HS512"], audience=config['CLIENT_ID'])

    return user_data


async def jinja_templates():
    return Jinja2Templates(directory="app/view/templates")
