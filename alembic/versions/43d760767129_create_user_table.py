"""create user table

Revision ID: 43d760767129
Revises: 00eec6c7a4f1
Create Date: 2021-12-01 17:39:00.285770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43d760767129'
down_revision = '00eec6c7a4f1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                           server_default=sa.text('Now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                    
                    )   
    pass


def downgrade():
    op.drop_table('users')
    pass
