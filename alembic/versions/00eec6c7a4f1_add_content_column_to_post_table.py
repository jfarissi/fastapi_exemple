"""add content column to  post table

Revision ID: 00eec6c7a4f1
Revises: ffc2aef3723b
Create Date: 2021-12-01 17:29:22.794812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00eec6c7a4f1'
down_revision = 'ffc2aef3723b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
