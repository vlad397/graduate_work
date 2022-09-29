from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from core.config import config
from flask_apispec import FlaskApiSpec
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/swagger'


def prepare_docs(app):
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='api',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0",
        ),
    })
    docs = FlaskApiSpec(app)

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': config.project_name}
    )

    app.register_blueprint(swagger_ui_blueprint)
    from api.v1 import routes
    from api.v1.permission.check import check_permission
    from api.v1.permission.grant import grant_permission
    from api.v1.permission.take import take_permission
    from api.v1.role.change import change_role
    from api.v1.role.create import create_role
    from api.v1.role.delete import delete_role
    from api.v1.role.list import list_role
    from api.v1.user.change_password import (change_password,
                                             change_password_google)
    from api.v1.user.history import history
    from api.v1.user.login import login
    from api.v1.user.logout import logout
    from api.v1.user.oauth import authorize_oauth, login_oauth
    from api.v1.user.profile import profile
    from api.v1.user.refresh_token import refresh
    from api.v1.user.registration import registration

    docs.register(registration, blueprint=routes.name)
    docs.register(change_password, blueprint=routes.name)
    docs.register(history, blueprint=routes.name)
    docs.register(login, blueprint=routes.name)
    docs.register(logout, blueprint=routes.name)
    docs.register(profile, blueprint=routes.name)
    docs.register(refresh, blueprint=routes.name)
    docs.register(change_role, blueprint=routes.name)
    docs.register(create_role, blueprint=routes.name)
    docs.register(delete_role, blueprint=routes.name)
    docs.register(list_role, blueprint=routes.name)
    docs.register(take_permission, blueprint=routes.name)
    docs.register(grant_permission, blueprint=routes.name)
    docs.register(check_permission, blueprint=routes.name)
    docs.register(change_password_google, blueprint=routes.name)
    docs.register(login_oauth, blueprint=routes.name)
    docs.register(authorize_oauth, blueprint=routes.name)

    # black magic for delete options
    for key, value in docs.spec._paths.items():
        docs.spec._paths[key] = {
            inner_key: inner_value
            for inner_key, inner_value in value.items()
            if inner_key != 'options'
        }
