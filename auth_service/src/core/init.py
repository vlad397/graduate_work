import hashlib

import click
import redis
from authlib.integrations.flask_client import OAuth
from decorators.bucket import Bucket
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

from .config import config
from .docs import prepare_docs
from .oauth import registrate_services


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='localhost',
                agent_port=6831,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


configure_tracer()
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
redis_db = redis.Redis(host=config.redis_host, port=config.redis_port)
bucket = Bucket(redis_db, config.limit_requests)
oauth = OAuth()


def create_app():
    app = Flask(__name__)
    user = config.postrges_user
    password = config.postrges_pass
    db_host = config.postrges_host
    db_name = config.postrges_db
    connection = f"postgresql://{user}:{password}@{db_host}/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = connection
    app.config["SECRET_KEY"] = config.secret_key
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.jwt_access_expire
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.jwt_expire
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    from api import v1
    app.register_blueprint(v1.routes)
    oauth.init_app(app, cache=redis_db)
    registrate_services(oauth)
    prepare_docs(app)
    FlaskInstrumentor().instrument_app(app)

    @app.cli.command('create_superuser')
    @click.argument("name")
    @click.argument("email")
    @click.argument("password_super")
    def create_superuser(name, email, password_super):
        from db.role import Role
        from db.user import Users
        from db.user_role import UserRole
        from handler.user_handler import ADMIN_ROLE, DEFAULT_ROLE
        cur_user = Users(username=name, email=email,
                         password=hashlib.md5(f"{password_super}{config.salt}".encode()).hexdigest())
        cur_user.save()
        superuser_role = Role.find_by_name(ADMIN_ROLE)
        UserRole(user_id=user.id, role_id=superuser_role.id).save()
        default_role = Role.find_by_name(DEFAULT_ROLE)
        UserRole(user_id=user.id, role_id=default_role.id).save()
    return app

