from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from decorators.user_checks import admin_required, logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields


class ChangeRoleSchema(Schema):
    new_name = fields.String(required=True)
    old_name = fields.String(required=True)


@routes.route('/change_role', methods=['PATCH'])
@marshal_with(ResponseSchema())
@use_kwargs(ChangeRoleSchema())
@doc(description='Method for change role', tags=['role'], params=params_auth_default)
@jwt_required()
@admin_required()
@logout_session()
def change_role(**kwargs):

    new_name = kwargs.get('new_name')
    old_name = kwargs.get('old_name')

    if new_name == old_name:
        return {MESSAGE: 'Same name'}, HTTPStatus.FORBIDDEN

    role = Role.find_by_name(old_name)
    if not role:
        return {MESSAGE: 'No such role'}, HTTPStatus.FORBIDDEN
    role.name = new_name
    role.save()
    return {MESSAGE: 'Profile not found'}, HTTPStatus.OK
