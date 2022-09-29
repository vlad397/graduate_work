"""empty message

Revision ID: 40ee531e8a72
Revises: 4e928ec17057
Create Date: 2022-06-06 05:20:06.325378

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '40ee531e8a72'
down_revision = '4e928ec17057'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ip_address', sa.String(length=256), nullable=True),
    sa.Column('browser', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'browser'),
    sa.UniqueConstraint('id', 'browser'),
    postgresql_partition_by='LIST (browser)'
    )
    op.create_unique_constraint(None, 'role', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    op.create_unique_constraint(None, 'users_role', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_role', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    op.drop_table('history')
    # ### end Alembic commands ###