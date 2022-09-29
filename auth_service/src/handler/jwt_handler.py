import jwt
from core.config import config
from core.init import redis_db
from db.role import Role
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import Schema, fields


class JWTToken(Schema):
    access_token = fields.String(required=False)
    refresh_token = fields.String(required=False)


def generate_access_token(user_id: str, permissions):
    access_token = create_access_token(identity=user_id, additional_claims=permissions)
    return access_token


def generate_jwt(user_id: str) -> JWTToken:
    roles = Role.get_roles_by_user_id(user_id)
    permissions = {'permissions': [r.name for r in roles]}
    access_token = generate_access_token(user_id, permissions)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=permissions)
    jti = jwt.decode(jwt=refresh_token, key=config.secret_key, algorithms=config.jwt_algorithm).get("jti")
    redis_db.set(str(jti), str(user_id), ex=config.jwt_expire)
    return JWTToken().load({'access_token': access_token, 'refresh_token': refresh_token})
