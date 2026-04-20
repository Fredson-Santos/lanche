"""Add alertas table and fields for RF-01, RF-02, RF-03

Revision ID: a1b2c3d4e5f6
Revises: 3fb9114d1997
Create Date: 2026-04-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '3fb9114d1997'
branch_labels: Union[Sequence[str], None] = None
depends_on: Union[Sequence[str], None] = None


def upgrade() -> None:
    # ### Add fields to Produto table ###
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_validade', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('lote', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('temperatura_ideal_min', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('temperatura_ideal_max', sa.Float(), nullable=True))

    # ### Add fields to Estoque table ###
    with op.batch_alter_table('estoques', schema=None) as batch_op:
        batch_op.add_column(sa.Column('temperatura_atual', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('data_ultima_verificacao', sa.DateTime(timezone=True), nullable=True))

    # ### Create Alerta table ###
    op.create_table('alertas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('estoque_id', sa.Integer(), nullable=True),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('titulo', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('lido', sa.Boolean(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('data_leitura', sa.DateTime(timezone=True), nullable=True),
    sa.Column('data_resolucao', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['estoque_id'], ['estoques.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    with op.batch_alter_table('alertas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_alertas_ativo'), ['ativo'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_data_criacao'), ['data_criacao'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_estoque_id'), ['estoque_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_lido'), ['lido'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_produto_id'), ['produto_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_alertas_tipo'), ['tipo'], unique=False)


def downgrade() -> None:
    # ### Drop Alerta table ###
    with op.batch_alter_table('alertas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_alertas_tipo'))
        batch_op.drop_index(batch_op.f('ix_alertas_produto_id'))
        batch_op.drop_index(batch_op.f('ix_alertas_lido'))
        batch_op.drop_index(batch_op.f('ix_alertas_id'))
        batch_op.drop_index(batch_op.f('ix_alertas_estoque_id'))
        batch_op.drop_index(batch_op.f('ix_alertas_data_criacao'))
        batch_op.drop_index(batch_op.f('ix_alertas_ativo'))

    op.drop_table('alertas')

    # ### Remove fields from Estoque table ###
    with op.batch_alter_table('estoques', schema=None) as batch_op:
        batch_op.drop_column('data_ultima_verificacao')
        batch_op.drop_column('temperatura_atual')

    # ### Remove fields from Produto table ###
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.drop_column('temperatura_ideal_max')
        batch_op.drop_column('temperatura_ideal_min')
        batch_op.drop_column('lote')
        batch_op.drop_column('data_validade')
