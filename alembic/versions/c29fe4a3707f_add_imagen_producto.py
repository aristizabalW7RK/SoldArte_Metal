"""add_imagen_producto

Revision ID: c29fe4a3707f
Revises: 0227f8f27c96
Create Date: 2026-06-18 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c29fe4a3707f'
down_revision: Union[str, None] = '0227f8f27c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('imagen_producto',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('es_portada', sa.Boolean(), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_imagen_producto_id'), 'imagen_producto', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_imagen_producto_id'), table_name='imagen_producto')
    op.drop_table('imagen_producto')
