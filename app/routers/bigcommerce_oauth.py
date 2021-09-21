import bigcommerce
from bigcommerce.api import BigcommerceApi
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select

from app.config import config
from app.db import engine
from app.dependencies import verified_payload, jinja_templates
from app.models import Store, User, StoreUserScope


router = APIRouter(
    prefix="/bigcommerce/oauth",
    tags=["Auth"],
)


## Single click oauth callback https://developer.bigcommerce.com/api-docs/partner/getting-started/app-development/single-click-apps/single-click-app-oauth-flow
@router.get('/callback')
def auth_callback(request: Request, code: str, context: str, scope: str, templates: Jinja2Templates = Depends(jinja_templates)):
    session = Session(engine)

    store_hash = context.split('/')[1]

    store = session.exec(select(Store).where(Store.store_hash == store_hash)).first()
    if store is None:
        redirect = request.url_for('auth_callback')
        api = bigcommerce.api.BigcommerceApi(client_id=config['CLIENT_ID'], store_hash=store_hash)
        token = api.oauth_fetch_token(config['CLIENT_SECRET'], code, context, scope, redirect)

        store = Store(store_hash=store_hash, access_token=token['access_token'], scope=scope)
        session.add(store)

        user = session.exec(select(User).where(User.bc_id == 2073294)).first()
        if user is None:
            user = User(bc_id=token['user']['id'], email=token['user']['email'])
            session.add(user)

    user = session.exec(select(User).where(User.bc_id == 2073294)).first()
    user.stores.append(store)

    session.commit()

    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "store": store})


## Single click load https://developer.bigcommerce.com/api-docs/apps/guide/callbacks
@router.get('/load')
def load(request: Request, user_data: dict = Depends(verified_payload), templates: Jinja2Templates = Depends(jinja_templates)):
    session = Session(engine)

    store = session.exec(select(Store).where(Store.store_hash == user_data['store_hash'])).first()
    if store is None:
        raise Exception('Invalid store {}'.format(user_data['store_hash']))

    user = session.exec(select(User).where(User.bc_id == user_data['user']['id'])).first()
    if user is None:
        user = User(bc_id=user_data['user']['id'], email=user_data['user']['email'])
        session.add(user)
        session.commit()

    if user not in store.users:
        store.users.append(user)
        session.commit()

    scope = session.exec(select(StoreUserScope).where(Store.id == store.id and User.id == user.id)).first()
    if scope is None:
        is_owner=user_data['user']['id'] == user_data['owner']['id']
        scope = StoreUserScope(
            store_id=store.id,
            user_id=user.id,
            is_owner=is_owner
        )
        session.add(scope)
        session.commit()

    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "store": store})

## Single click uninstall https://developer.bigcommerce.com/api-docs/apps/guide/callbacks
@router.get('/uninstall')
def uninstall(user_data: dict = Depends(verified_payload)):
    session = Session(engine)

    store_hash = user_data['store_hash']
    store = session.exec(select(Store).where(Store.store_hash == store_hash)).first()
    if store is None:
        raise Exception('Store does not exist')

    for user in store.users:
        session.delete(user)

    session.delete(store)
    session.delete(store)
    session.commit()

    return Response(None, status_code=204)

## Single click remove-user https://developer.bigcommerce.com/api-docs/apps/guide/callbacks
@router.get('/remove-user')
def remove_user(user_data: dict = Depends(verified_payload)):
    session = Session(engine)

    user = session.exec(select(User).where(User.bc_id == user_data['user']['id'])).first()
    if user is not None:
        session.delete(user)
        session.commit()

    return Response(None, status_code=204)
