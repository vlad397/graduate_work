from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from db.user import Users
from db.user_role import UserRole
from decorators.user_checks import admin_required, logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields


class DeletePermissionSchema(Schema):
    role_name = fields.String(required=True)
    username = fields.String(required=True)


@routes.route('/take_permission', methods=['DELETE'])
@marshal_with(ResponseSchema())
@use_kwargs(DeletePermissionSchema())
@doc(description='Method for take permission', tags=['permission'], params=params_auth_default)
@jwt_required()
@admin_required()
@logout_session()
def take_permission(**kwargs):
    username = kwargs.get('username')
    role_name = kwargs.get('role_name')
    user = Users.find_by_username(username)
    if not user:
        return {MESSAGE: 'No such user'}, HTTPStatus.FORBIDDEN
    role = Role.find_by_name(role_name)
    if not role:
        return {MESSAGE: 'No such role'}, HTTPStatus.FORBIDDEN
    user_role = UserRole.find_permission(user.id, role.id)
    if not user_role:
        return {MESSAGE: 'No such permission'}, HTTPStatus.FORBIDDEN
    user_role.delete()
    return {MESSAGE: 'Delete permission'}, HTTPStatus.OK
