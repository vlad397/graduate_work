from core.init import db
from sqlalchemy import DateTime, String, func

from .base import BaseModel
from .user_role import UserRole


class Role(BaseModel):
    __tablename__ = "role"

    modified = db.Column(DateTime, default=func.now())
    name = db.Column(String(length=256), nullable=False, unique=True)

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def get_roles_by_user_id(cls, user_id: str):
        return cls.query.join(UserRole).filter(UserRole.user_id == user_id).all()


