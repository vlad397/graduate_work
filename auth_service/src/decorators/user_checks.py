from functools import wraps
from http import HTTPStatus

from constants.response import MESSAGE
from db.role import Role
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from handler.user_handler import ADMIN_ROLE, is_logout


def logout_session():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            jti = str(get_jwt().get('jti'))
            if is_logout(jti):
                return {MESSAGE: 'Logged out'}, HTTPStatus.BAD_REQUEST
            else:
                return func(*args, **kwargs)
        return decorator
    return wrapper


def admin_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            roles = Role.get_roles_by_user_id(user_id)
            if ADMIN_ROLE in [r.name for r in roles]:
                return func(*args, **kwargs)
            else:
                return {MESSAGE: 'Only for superuser'}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper
