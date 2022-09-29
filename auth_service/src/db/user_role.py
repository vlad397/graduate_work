import uuid

from core.init import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class UserRole(BaseModel):
    __tablename__ = "users_role"

    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), default=uuid.uuid4, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), default=uuid.uuid4, nullable=False)

    @classmethod
    def delete_by_role_id(cls, role_id: str):
        cls.query.filter_by(role_id=role_id).delete(synchronize_session=False)
        db.session.commit()

    @classmethod
    def find_permission(cls, user_id: str, role_id: str):
        return cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).one_or_none()
