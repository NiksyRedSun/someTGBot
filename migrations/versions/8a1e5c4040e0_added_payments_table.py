"""Added payments table

Revision ID: 8a1e5c4040e0
Revises: 7d8eb682c984
Create Date: 2024-04-25 23:24:22.605281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a1e5c4040e0'
down_revision: Union[str, None] = '7d8eb682c984'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Payments',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('ClientId', sa.BigInteger(), nullable=True),
    sa.Column('Sum', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ClientId'], ['Clients.Id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Payments')
    # ### end Alembic commands ###
