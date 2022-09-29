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


class CreateRoleSchema(Schema):
    name = fields.String(required=True)


@routes.route('/create_role', methods=['POST'])
@marshal_with(ResponseSchema())
@use_kwargs(CreateRoleSchema())
@doc(description='Method for create role', tags=['role'], params=params_auth_default)
@jwt_required()
@admin_required()
@logout_session()
def create_role(**kwargs):
    new_name_role = kwargs.get('name')
    role = Role.find_by_name(new_name_role)
    if role:
        return {MESSAGE: 'Already exists such role'}, HTTPStatus.FORBIDDEN
    Role(name=new_name_role).save()
    return {MESSAGE: 'Created new role'}, HTTPStatus.OK
