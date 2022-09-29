import hashlib
from http import HTTPStatus

from api.v1 import routes
from api.v1.user.login import LoginResponseSchema
from constants import NO_PASSWORD_PLACEHOLDER
from constants.response import MESSAGE
from core.config import config
from core.init import oauth
from core.oauth import OAuthServices
from db.provider_user import ProviderUsers
from db.user import Users
from flask import request, url_for
from flask_apispec import doc, marshal_with, use_kwargs
from handler.jwt_handler import generate_jwt
from handler.user_handler import make_user_history_record, registrate
from marshmallow import Schema, fields


class OAuthLoginSchema(Schema):
    provider = fields.String(required=True)


@routes.route('/login_oauth',  methods=['GET'])
@use_kwargs(OAuthLoginSchema(), location='query')
@doc(description='Method for login oauth', tags=['users'])
def login_oauth(**kwargs):
    provider = kwargs['provider']
    if not OAuthServices.has_value(provider):
        return {MESSAGE: 'Provider not found'}, HTTPStatus.BAD_REQUEST
    client = getattr(oauth, provider)
    redirect_uri = url_for('.authorize_oauth', provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri=redirect_uri)


class OAuthLoginResponseSchema(LoginResponseSchema):
    username = fields.String(required=False)


@routes.route('/authorize_oauth', methods=['GET', 'POST'])
@marshal_with(OAuthLoginResponseSchema())
@use_kwargs(OAuthLoginSchema(), location='query')
@doc(description='Method for authorize google', tags=['users'])
def authorize_oauth(**kwargs):
    provider = kwargs['provider']
    if not OAuthServices.has_value(provider):
        return {MESSAGE: 'Provider not found'}, HTTPStatus.BAD_REQUEST
    client = getattr(oauth, provider)
    token = client.authorize_access_token()
    email = token['userinfo']['email']
    user = Users.find_by_email(email)
    additional_info = {}
    if not user:
        username = hashlib.md5(f"{email}{config.salt_user}".encode()).hexdigest()
        registrate(username, email, NO_PASSWORD_PLACEHOLDER, False, True)
        user = Users.find_by_email(email)
        ProviderUsers(internal_user_id=user.id, provider=provider).save()
    additional_info['username'] = user.username
    jwt = generate_jwt(user.id)
    make_user_history_record(user.id, request.remote_addr, request.user_agent.browser)
    return {MESSAGE: 'Successful login', **additional_info,  **jwt}, HTTPStatus.OK
