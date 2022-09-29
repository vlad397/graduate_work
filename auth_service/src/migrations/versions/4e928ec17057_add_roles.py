"""empty message

Revision ID: 4e928ec17057
Revises: 42ba7f6eef71
Create Date: 2022-06-05 12:02:49.000212

"""
import db.role as role
from alembic import op

# revision identifiers, used by Alembic.
revision = '4e928ec17057'
down_revision = '42ba7f6eef71'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        role.Role.__table__,
        [
            {
                "name": "premium",
            },
            {
                "name": "superuser",
            },
        ],
    )

def downgrade():
    pass
