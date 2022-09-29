"""empty message

Revision ID: 817e72d91db4
Revises: 40ee531e8a72
Create Date: 2022-06-06 14:08:21.128826

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '817e72d91db4'
down_revision = '40ee531e8a72'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
            CREATE TABLE IF NOT EXISTS "history_mozilla" PARTITION OF "history" FOR VALUES IN ('Mozilla');
            CREATE TABLE IF NOT EXISTS "history_unknown" PARTITION OF "history" FOR VALUES IN ('Unknown');
            CREATE TABLE IF NOT EXISTS "history_apple" PARTITION OF "history" FOR VALUES IN ('AppleWebKit');
            CREATE TABLE IF NOT EXISTS "history_chrome" PARTITION OF "history" FOR VALUES IN ('Chrome');
            CREATE TABLE IF NOT EXISTS "history_safari" PARTITION OF "history" FOR VALUES IN ('Safari');""")


def downgrade():
    pass
