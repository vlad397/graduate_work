from core.init import db
from sqlalchemy import ForeignKey, String, Text, desc
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class History(BaseModel):
    __tablename__ = "history"
    __table_args__ = (
        {
            'postgresql_partition_by': 'LIST (browser)'
        }
    )

    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ip_address = db.Column(String(length=256))
    browser = db.Column(Text(), nullable=False, primary_key=True)

    @classmethod
    def get_history_by_user_id(cls, user_id: str, num: int, page: int):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.created)).limit(num).offset(num*page)
