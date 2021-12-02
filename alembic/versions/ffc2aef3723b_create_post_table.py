"""create post table

Revision ID: ffc2aef3723b
Revises: 
Create Date: 2021-12-01 12:39:35.510137

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import String


# revision identifiers, used by Alembic.
revision = 'ffc2aef3723b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                   sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
