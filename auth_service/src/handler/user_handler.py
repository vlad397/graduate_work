import hashlib
import re
from http import HTTPStatus
import requests

from constants import BROWSERS, UNKNOWN_BROWSER_PLACEHOLDER
from constants.response import MESSAGE
from core.config import config
from core.init import redis_db
from db.history import History
from db.role import Role
from db.user import Users
from db.user_role import UserRole
from flask_restful import abort

DEFAULT_ROLE = 'premium'
ADMIN_ROLE = 'superuser'


def check_email_correct(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def check_username_correct(username: str) -> bool:
    regex = '^[a-zA-Z0-9_.-]*$'
    if re.fullmatch(regex, username):
        return True
    return False


def registrate(username: str, email: str, password: str, hash_pass: bool = True, verified: bool = False):
    default_role = Role().find_by_name(DEFAULT_ROLE)
    if not default_role:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            message={MESSAGE: 'No default role'},
        )
    if hash_pass:
        password = hashlib.md5(f"{password}{config.salt}".encode()).hexdigest()
    user = Users(username=username, email=email, password=password, email_verified=verified)
    user.save()
    user_role = UserRole(user_id=user.id, role_id=default_role.id)
    user_role.save()


def send_email_verification(user_id: str, token: str):
    data = {
        'user_id': user_id,
        'header': config.email_verify_header_name,
        'body': config.email_verify_body_name,
        'channel_id': config.verify_channel,
        'user_endpoint': f'{config.server_url}/api/v1/verify_email?token={token}'
    }
    # requests.post(config.notification_service_endpoint, json=data, headers={'content-type': 'application/json'})


def validate_pass(username: str, password: str):
    hash_password = hashlib.md5(f"{password}{config.salt}".encode()).hexdigest()
    return Users.find_by_username_password(username).password == hash_password


def make_user_history_record(user_id: str, ip_address: str, browser: str) -> None:
    if browser not in BROWSERS:
        browser = UNKNOWN_BROWSER_PLACEHOLDER
    History(user_id=user_id, ip_address=ip_address, browser=browser).save()


def is_logout(jti: str) -> str:
    return redis_db.get(jti)
