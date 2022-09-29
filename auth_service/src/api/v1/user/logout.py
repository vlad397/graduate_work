from http import HTTPStatus

from api.v1 import routes
from api.v1.common import ResponseSchema
from constants.doc_params import params_auth_default
from constants.response import MESSAGE
from core.init import redis_db
from flask_apispec import doc, marshal_with
from flask_jwt_extended import get_jwt, jwt_required


@routes.route('/logout', methods=['POST'])
@marshal_with(ResponseSchema())
@doc(description='Method for logout', tags=['users'], params=params_auth_default)
@jwt_required()
def logout():
    jti = get_jwt().get("jti")

    if redis_db.get(str(jti)):
        redis_db.delete(str(jti))

    return {MESSAGE: 'Successful logout'}, HTTPStatus.OK
