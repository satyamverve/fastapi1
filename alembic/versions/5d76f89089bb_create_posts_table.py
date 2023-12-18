"""create posts table

Revision ID: 5d76f89089bb
Revises: 243f3e5bc398
Create Date: 2023-12-08 13:55:20.031342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d76f89089bb'
down_revision: Union[str, None] = '243f3e5bc398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',sa.Integer(), primary_key=True,index=True, nullable=False),
                    sa.Column('title',sa.String(50), nullable=False),
                    sa.Column('content',sa.String(250), nullable=False),
                    sa.Column('published',sa.String(50), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()')),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'))
    pass


def downgrade() :
    op.drop_table('posts')
    pass
