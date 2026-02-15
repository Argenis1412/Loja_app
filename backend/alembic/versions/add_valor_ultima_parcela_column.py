"""add valor_ultima_parcela column

Revision ID: add_valor_ultima_parcela
Revises: 4031dc3f14ce
Create Date: 2026-02-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_valor_ultima_parcela'
down_revision: Union[str, None] = '4031dc3f14ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar la columna valor_ultima_parcela a la tabla recibos
    op.add_column('recibos', sa.Column('valor_ultima_parcela', sa.Float(), nullable=True))


def downgrade() -> None:
    # Eliminar la columna valor_ultima_parcela de la tabla recibos
    op.drop_column('recibos', 'valor_ultima_parcela')
