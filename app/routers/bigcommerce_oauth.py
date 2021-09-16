import bigcommerce
from bigcommerce.api import BigcommerceApi
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.config import config
from app.db import engine
from app.models import Store, User

router = APIRouter(
    prefix="/bigcommerce/oauth",
    tags=["Auth"],
)


@router.get('/callback')
def auth_callback(request: Request, code: str, context: str, scope: str):
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

    ## TODO Redirect correctly so we don't get a payload error on /load
    return RedirectResponse(request.url_for('load'))


# The Load URL. See https://developer.bigcommerce.com/api/load
@router.get('/load')
def load(signed_payload):
    try:
        user_data = BigcommerceApi.oauth_verify_payload(signed_payload, config['CLIENT_SECRET'])
    except Exception as e:
        raise e

    # TODO Create / update user entity
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

    # TODO Return actual app dashboard
    return {"message": "Hello {}".format(user.email)}
#
# # The Uninstall URL. See https://developer.bigcommerce.com/api/load
# @router.route('/bigcommerce/uninstall')
# def uninstall():
#     # Decode and verify payload
#     payload = flask.request.args['signed_payload_jwt']
#     try:
#         user_data = BigcommerceApi.oauth_verify_payload_jwt(payload, client_secret(), client_id())
#     except Exception as e:
#         return jwt_error(e)
#
#     # Lookup store
#     store_hash = user_data['sub'].split('stores/')[1]
#     store = Store.query.filter_by(store_hash=store_hash).first()
#     if store is None:
#         return "Store not found!", 401
#
#     # Clean up: delete store associated users. This logic is up to you.
#     # You may decide to keep these records around in case the user installs
#     # your app again.
#     storeusers = StoreUser.query.filter_by(store_id=store.id)
#     for storeuser in storeusers:
#         db.session.delete(storeuser)
#     db.session.delete(store)
#     db.session.commit()
#
#     return flask.Response('Deleted', status=204)
#
#
# # The Remove User Callback URL.
# @router.route('/bigcommerce/remove-user')
# def remove_user():
#     payload = flask.request.args['signed_payload_jwt']
#     try:
#         user_data = BigcommerceApi.oauth_verify_payload_jwt(payload, client_secret(), client_id())
#     except Exception as e:
#         return jwt_error(e)
#
#     store_hash = user_data['sub'].split('stores/')[1]
#     store = Store.query.filter_by(store_hash=store_hash).first()
#     if store is None:
#         return "Store not found!", 401
#
#     # Lookup user and delete it
#     bc_user_id = user_data['user']['id']
#     user = User.query.filter_by(bc_id=bc_user_id).first()
#     if user is not None:
#         storeuser = StoreUser.query.filter_by(user_id=user.id, store_id=store.id).first()
#         db.session.delete(storeuser)
#         db.session.commit()
#
#     return flask.Response('Deleted', status=204)
