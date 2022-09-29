from constants import NO_PASSWORD_PLACEHOLDER
from core.init import db
from sqlalchemy import DateTime, String, and_, func, Boolean

from .base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    username = db.Column(String(length=256), nullable=False, unique=True)
    modified = db.Column(DateTime, default=func.now())
    password = db.Column(String(length=256), nullable=False)
    email = db.Column(String(length=256), nullable=False, unique=True)
    email_verified = db.Column(Boolean(), nullable=False, default=False)

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def find_by_username_password(cls, username: str):
        return cls.query \
            .filter(and_(Users.username == username, Users.password != NO_PASSWORD_PLACEHOLDER)).one_or_none()

    @classmethod
    def find_by_user_id(cls, user_id: str):
        return cls.query.filter_by(id=user_id).one_or_none()
