"""Add ordem_reposicao table and restock fields for RF-06

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-04-19 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[Sequence[str], None] = None
depends_on: Union[Sequence[str], None] = None


def upgrade() -> None:
    # ### Add fields to Estoque table for restock management ###
    with op.batch_alter_table('estoques', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estoque_minimo', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('estoque_maximo', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('ponto_reposicao', sa.Integer(), nullable=True))

    # ### Create OrdemReposicao table ###
    op.create_table('ordens_reposicao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estoque_id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('quantidade_solicitada', sa.Integer(), nullable=False),
    sa.Column('quantidade_recebida', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('motivo', sa.String(length=255), nullable=True),
    sa.Column('observacoes', sa.Text(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('data_confirmacao', sa.DateTime(timezone=True), nullable=True),
    sa.Column('data_recebimento', sa.DateTime(timezone=True), nullable=True),
    sa.Column('data_cancelamento', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['estoque_id'], ['estoques.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    with op.batch_alter_table('ordens_reposicao', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ordens_reposicao_data_criacao'), ['data_criacao'], unique=False)
        batch_op.create_index(batch_op.f('ix_ordens_reposicao_estoque_id'), ['estoque_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_ordens_reposicao_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_ordens_reposicao_produto_id'), ['produto_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_ordens_reposicao_status'), ['status'], unique=False)


def downgrade() -> None:
    # ### Drop OrdemReposicao table ###
    with op.batch_alter_table('ordens_reposicao', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ordens_reposicao_status'))
        batch_op.drop_index(batch_op.f('ix_ordens_reposicao_produto_id'))
        batch_op.drop_index(batch_op.f('ix_ordens_reposicao_id'))
        batch_op.drop_index(batch_op.f('ix_ordens_reposicao_estoque_id'))
        batch_op.drop_index(batch_op.f('ix_ordens_reposicao_data_criacao'))

    op.drop_table('ordens_reposicao')

    # ### Remove fields from Estoque table ###
    with op.batch_alter_table('estoques', schema=None) as batch_op:
        batch_op.drop_column('ponto_reposicao')
        batch_op.drop_column('estoque_maximo')
        batch_op.drop_column('estoque_minimo')
