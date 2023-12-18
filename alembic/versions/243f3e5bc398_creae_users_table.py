"""creae users table

Revision ID: 243f3e5bc398
Revises: 
Create Date: 2023-12-08 13:10:15.547294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '243f3e5bc398'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(), primary_key=True,index=True, nullable=False),
                    sa.Column('username',sa.String(50), nullable=False),
                    sa.Column('email',sa.String(50), nullable=False),
                    sa.Column('password',sa.String(50), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_table('users')
    pass
