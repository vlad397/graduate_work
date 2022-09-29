import uuid

from core.init import db
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class ProviderUsers(BaseModel):
    __tablename__ = "provider_users"

    internal_user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), default=uuid.uuid4, nullable=False)
    provider = db.Column(String(length=256), nullable=False)

    @classmethod
    def find_by_internal_user_id(cls, internal_user_id: str):
        return cls.query.filter_by(internal_user_id=internal_user_id).one_or_none()
