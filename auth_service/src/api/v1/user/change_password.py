import hashlib
from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants import NO_PASSWORD_PLACEHOLDER
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from core.config import config
from db.user import Users
from decorators.user_checks import logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields


class ChangePasswordSchema(Schema):
    password = fields.String(required=True)


@routes.route('/change_password', methods=['PATCH'])
@use_kwargs(ChangePasswordSchema())
@marshal_with(ResponseSchema())
@doc(description='Method for changing password', tags=['users'], params=params_auth_default)
@jwt_required()
@logout_session()
def change_password(**kwargs):
    new_password = kwargs.get('password')
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    new_password_hash = hashlib.md5(f"{new_password}{config.salt}".encode()).hexdigest()
    if user.password == new_password_hash:
        return {MESSAGE: 'Same password'}, HTTPStatus.BAD_REQUEST
    user.password = new_password_hash
    user.save()
    return {MESSAGE: 'Successfully changed'}, HTTPStatus.OK


@routes.route('/change_password_google', methods=['PATCH'])
@use_kwargs(ChangePasswordSchema())
@marshal_with(ResponseSchema())
@doc(description='Method for changing password after google registration', tags=['users'], params=params_auth_default)
@jwt_required()
@logout_session()
def change_password_google(**kwargs):
    new_password = kwargs.get('password')
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    if user.password != NO_PASSWORD_PLACEHOLDER:
        return {MESSAGE: 'Already changed'}, HTTPStatus.BAD_REQUEST
    user.password = hashlib.md5(f"{new_password}{config.salt}".encode()).hexdigest()
    user.save()
    return {MESSAGE: 'Successfully changed'}, HTTPStatus.OK
