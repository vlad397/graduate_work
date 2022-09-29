from flask import Blueprint

routes = Blueprint('v1', __name__, url_prefix='/api/v1')

from .permission import check, grant, take
from .role import change, create, delete, list
from .user import (change_password, history, login, logout, oauth, profile,
                   refresh_token, registration)
