"""db creation

Revision ID: ebd6aa77a2a8
Revises: 
Create Date: 2024-04-23 16:11:19.566325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebd6aa77a2a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Clients',
    sa.Column('Id', sa.BigInteger(), nullable=False),
    sa.Column('First Name', sa.String(), nullable=True),
    sa.Column('Last Name', sa.String(), nullable=True),
    sa.Column('Middle Name', sa.String(), nullable=True),
    sa.Column('Address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Indicators',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('ClientId', sa.BigInteger(), nullable=True),
    sa.Column('Source', sa.String(), nullable=True),
    sa.Column('RoomType', sa.String(), nullable=True),
    sa.Column('FirstParameter', sa.Integer(), nullable=True),
    sa.Column('SecondParameter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ClientId'], ['Clients.Id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Treatments',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('ClientId', sa.BigInteger(), nullable=True),
    sa.Column('Text', sa.String(), nullable=True),
    sa.Column('Type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['ClientId'], ['Clients.Id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Treatments')
    op.drop_table('Indicators')
    op.drop_table('Clients')
    # ### end Alembic commands ###