"""paychange

Revision ID: 4dba88764fb7
Revises: 8a1e5c4040e0
Create Date: 2024-04-25 23:53:49.441917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4dba88764fb7'
down_revision: Union[str, None] = '8a1e5c4040e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Payments', sa.Column('CreatedOn', sa.DateTime(), nullable=True))
    op.drop_column('Payments', 'created_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Payments', sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('Payments', 'CreatedOn')
    # ### end Alembic commands ###
