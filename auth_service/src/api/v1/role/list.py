from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from db.role import Role
from decorators.user_checks import admin_required, logout_session
from flask_apispec import doc, marshal_with
from flask_jwt_extended import jwt_required
from marshmallow import fields


class ResponseRoleSchema(ResponseSchema):
    roles = fields.List(fields.String(), required=True)


@routes.route('/list_role', methods=['GET'])
@marshal_with(ResponseRoleSchema())
@doc(description='Method for list role', tags=['role'], params=params_auth_default)
@jwt_required()
@admin_required()
@logout_session()
def list_role():
    roles = Role.query.all()
    return {MESSAGE: 'All roles', 'roles': [r.name for r in roles]}, HTTPStatus.OK
