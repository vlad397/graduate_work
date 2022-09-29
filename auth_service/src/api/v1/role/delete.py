from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from db.user_role import UserRole
from decorators.user_checks import admin_required, logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields


class DeleteRoleSchema(Schema):
    name = fields.String(required=True)


@routes.route('/delete_role', methods=['DELETE'])
@marshal_with(ResponseSchema())
@use_kwargs(DeleteRoleSchema())
@doc(description='Method for delete role', tags=['role'], params=params_auth_default)
@jwt_required()
@admin_required()
@logout_session()
def delete_role(**kwargs):
    delete_name_role = kwargs.get('name')
    role = Role.find_by_name(delete_name_role)
    if not role:
        return {MESSAGE: 'No such role'}, HTTPStatus.FORBIDDEN
    UserRole.delete_by_role_id(role.id)
    role.delete()
    return {MESSAGE: 'Deleted role'}, HTTPStatus.OK
