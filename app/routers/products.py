import bigcommerce
from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import select, Session

from app.config import config
from app.db import engine
from app.dependencies import verified_bearer_header
from app.models import Store

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

## Single click oauth callback https://developer.bigcommerce.com/api-docs/partner/getting-started/app-development/single-click-apps/single-click-app-oauth-flow
@router.get('/')
def list(user_data: dict = Depends(verified_bearer_header)):
    session = Session(engine)
    store_hash = user_data['sub'].split('/').pop()
    store = session.exec(select(Store).where(Store.store_hash == store_hash)).first()
    api = bigcommerce.api.BigcommerceApi(client_id=config['CLIENT_ID'], store_hash=store_hash, access_token=store.access_token)

    products_all = api.Products.all()
    result = []
    for product in products_all:
        result.append(jsonable_encoder(product, exclude={'_connection'}))

    return {"products": result}
