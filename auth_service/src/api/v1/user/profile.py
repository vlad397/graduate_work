from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.user import Users
from decorators.user_checks import logout_session
from flask_apispec import doc, marshal_with
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import fields


class ProfileResponseSchema(ResponseSchema):
    username = fields.String(required=True)
    email = fields.String(required=True)


@routes.route('/profile', methods=['GET'])
@marshal_with(ProfileResponseSchema())
@doc(description='Method for profile', tags=['users'], params=params_auth_default)
@jwt_required()
@logout_session()
def profile():
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    if user:
        return {MESSAGE: 'Success', 'username': user.username, 'email': user.email}, HTTPStatus.OK
    return {MESSAGE: 'Profile not found'}, HTTPStatus.NOT_FOUND
