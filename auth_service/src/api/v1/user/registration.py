import hashlib
import random
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.response import MESSAGE
from core.init import redis_db
from db.user import Users
from flask_apispec import doc, marshal_with, use_kwargs
from handler.user_handler import (check_email_correct, check_username_correct,
                                  registrate, send_email_verification)
from marshmallow import Schema, fields


class RegistrationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)


@routes.route('/registration', methods=['POST'])
@use_kwargs(RegistrationSchema())
@marshal_with(ResponseSchema())
@doc(description='Method for registration', tags=['users'])
def registration(**kwargs):
    email = kwargs.get('email')
    username = kwargs.get('username')
    password = kwargs.get('password')

    if not check_email_correct(email):
        return {MESSAGE: 'Bad email address'}, HTTPStatus.BAD_REQUEST

    if not check_username_correct(username):
        return {MESSAGE: 'Bad email address'}, HTTPStatus.BAD_REQUEST

    if Users.find_by_email(email):
        return {MESSAGE: 'Such email already exists'}, HTTPStatus.BAD_REQUEST

    if Users.find_by_username(username):
        return {MESSAGE: 'Such username already exists'}, HTTPStatus.BAD_REQUEST

    registrate(username, email, password)
    user = Users.find_by_username(username)
    token = hashlib.md5(f"{user.id}{random.randint(0, 100_000)}".encode()).hexdigest()
    send_email_verification(user.id, token)

    return {MESSAGE: 'Successfully created'}, HTTPStatus.OK


@routes.route('/send_verification', methods=['GET'])
@marshal_with(ResponseSchema())
@doc(description='Method for sending verify email', tags=['users'])
@jwt_required()
def send_verification():
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    if user.email_verified:
        return {MESSAGE: 'Already verified'}, HTTPStatus.FORBIDDEN
    token = hashlib.md5(f"{user_id}{random.randint(0, 100_000)}".encode()).hexdigest()
    send_email_verification(user_id, token)
    redis_db.set(token, user_id)
    return {MESSAGE: 'Email sent'}, HTTPStatus.OK


class VerifySchema(Schema):
    token = fields.String(required=True)


@routes.route('/verify_email', methods=['GET'])
@marshal_with(ResponseSchema())
@use_kwargs(VerifySchema())
@doc(description='Method for verify email', tags=['users'])
@jwt_required()
def verify_email(**kwargs):
    token = kwargs.get('token')
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    if user.email_verified:
        return {MESSAGE: 'Already verified'}, HTTPStatus.FORBIDDEN
    user_id_cached = redis_db.get(token)
    if user_id_cached and user_id_cached == user_id:
        user.email_verified = True
        return {MESSAGE: 'Success'}, HTTPStatus.OK
    return {MESSAGE: 'Expired link'}, HTTPStatus.OK
