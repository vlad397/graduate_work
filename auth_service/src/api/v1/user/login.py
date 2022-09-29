from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.response import MESSAGE
from db.user import Users
from flask import request
from flask_apispec import doc, marshal_with, use_kwargs
from handler.jwt_handler import JWTToken, generate_jwt
from handler.user_handler import make_user_history_record, validate_pass
from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(ResponseSchema, JWTToken):
    pass


@routes.route('/login', methods=['POST'])
@use_kwargs(LoginSchema())
@marshal_with(LoginResponseSchema())
@doc(description='Method for login', tags=['users'])
def login(**kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    user = Users.find_by_username(username)

    if not user:
        return {MESSAGE: 'No such user or wrong password'}, HTTPStatus.BAD_REQUEST

    if not validate_pass(username, password):
        return {MESSAGE: 'No such user or wrong password'}, HTTPStatus.BAD_REQUEST

    jwt = generate_jwt(user.id)
    make_user_history_record(user.id, request.remote_addr, request.user_agent.browser)
    return {MESSAGE: 'Successful login', **jwt}, HTTPStatus.OK
