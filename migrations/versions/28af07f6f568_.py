"""empty message

Revision ID: 28af07f6f568
Revises: 1fc7e1e817b0
Create Date: 2025-01-13 15:39:41.595787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28af07f6f568'
down_revision = '1fc7e1e817b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('photographer', sa.String(length=150), nullable=True),
    sa.Column('photographerLink', sa.String(length=150), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('userName', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('link', sa.String(length=150), nullable=False),
    sa.Column('eventId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eventId'], ['event.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    op.drop_table('event')
    # ### end Alembic commands ###
