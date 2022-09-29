from http import HTTPStatus

from api.v1 import routes
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from core.init import bucket
from db.history import History
from db.user import Users
from decorators.user_checks import logout_session
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields


class HistoryResponseSchema(Schema):
    msg = fields.String(required=True)
    history = fields.List(fields.Dict)


class HistorySchema(Schema):
    num = fields.Int(required=False)
    page = fields.Int(required=False)


@routes.route('/history', methods=['GET'])
@marshal_with(HistoryResponseSchema())
@doc(description='Method for history', tags=['users'], params=params_auth_default)
@jwt_required()
@logout_session()
@use_kwargs(HistorySchema(), location='query')
@bucket.rate_limit
def history(**kwargs):
    user_id = get_jwt_identity()
    num = kwargs.get('num', 50)
    page = kwargs.get('page', 0)
    user = Users.find_by_user_id(user_id)
    if not user:
        return {MESSAGE: 'No such user'}, HTTPStatus.BAD_REQUEST
    hst = History.get_history_by_user_id(user.id, num, page)
    history_json = [
        {
            'username': user.username,
            'ip_address': h.ip_address,
            'browser': h.browser,
            'created': h.created,
        }
        for h in hst
    ]
    return {MESSAGE: 'Profile not found', 'history': history_json}, HTTPStatus.OK
