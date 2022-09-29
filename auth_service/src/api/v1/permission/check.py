from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from db.user import Users
from db.user_role import UserRole
from decorators.user_checks import logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields


class PermissionSchema(Schema):
    name = fields.String(required=True)


@routes.route('/check_permission', methods=['GET'])
@marshal_with(ResponseSchema())
@use_kwargs(PermissionSchema())
@doc(description='Method for check permission', tags=['permission'], params=params_auth_default)
@jwt_required()
@logout_session()
def check_permission(**kwargs):
    name = kwargs.get('name')
    user_id = get_jwt_identity()
    user = Users.find_by_user_id(user_id)
    if not user:
        return {MESSAGE: 'No such user'}, HTTPStatus.FORBIDDEN
    role = Role.find_by_name(name)
    if not role:
        return {MESSAGE: 'No such role'}, HTTPStatus.FORBIDDEN

    user_role = UserRole.find_permission(user.id, role.id)
    if not user_role:
        return {MESSAGE: 'No permission'}, HTTPStatus.FORBIDDEN
    return {MESSAGE: 'Have permission'}, HTTPStatus.OK
