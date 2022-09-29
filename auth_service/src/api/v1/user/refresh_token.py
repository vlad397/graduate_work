from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from flask_apispec import doc, marshal_with
from flask_jwt_extended import get_jwt_identity, jwt_required
from handler.jwt_handler import generate_access_token
from marshmallow import fields


class RefreshResponseSchema(ResponseSchema):
    access_token = fields.String(required=True)


@routes.route('/refresh', methods=['POST'])
@marshal_with(RefreshResponseSchema())
@doc(description='Method for refresh', tags=['users'], params=params_auth_default)
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    roles = Role.get_roles_by_user_id(user_id)
    permissions = {'permissions': [r.name for r in roles]}
    access_token = generate_access_token(user_id, permissions)
    return {MESSAGE: 'Successful refresh', 'access_token': access_token}, HTTPStatus.OK
