from bigcommerce.api import BigcommerceApi
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.config import config
import bigcommerce

router = APIRouter(
    prefix="/bigcommerce/oauth",
    tags=["Auth"],
)

@router.get('/callback')
def auth_callback(request: Request, code: str, context: str, scope: str):
    if config['token'] is None:
        store_hash = context.split('/')[1]
        redirect = request.url_for('auth_callback')

        api = bigcommerce.api.BigcommerceApi(client_id=config['CLIENT_ID'], store_hash=store_hash)
        token = api.oauth_fetch_token(config['CLIENT_SECRET'], code, context, scope, redirect)
        config['token'] = token

    ## TODO Create / Update store and user token

    return RedirectResponse(request.url_for('load'))


# The Load URL. See https://developer.bigcommerce.com/api/load
@router.get('/load')
def load(signed_payload):
    try:
        user_data = BigcommerceApi.oauth_verify_payload(signed_payload, config['CLIENT_SECRET'])
    except Exception as e:
        raise e

    # TODO Create / update user entity

    # TODO Return actual app dashboard
    return {"message": "Hello {}".format(user_data['user']['email'])}
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
