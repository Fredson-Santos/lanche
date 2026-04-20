"""Create api_keys table for RF-11 - APIs Abertas para Terceiros

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-04-19 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create api_keys table
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chave', sa.String(length=64), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('limite_requisicoes', sa.Integer(), nullable=False),
        sa.Column('janela_tempo', sa.Integer(), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ultima_uso', sa.DateTime(timezone=True), nullable=True),
        sa.Column('requisicoes_usadas', sa.Integer(), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.CheckConstraint('limite_requisicoes > 0', name='check_limite_requisicoes_positivo'),
        sa.CheckConstraint('janela_tempo > 0', name='check_janela_tempo_positiva'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_api_keys_chave_ativo', 'api_keys', ['chave', 'ativo'])
    op.create_index('ix_api_keys_criado_em', 'api_keys', ['criado_em'])
    op.create_index('ix_api_keys_expires_em', 'api_keys', ['expires_em'])
    op.create_unique_constraint('uq_api_keys_chave', 'api_keys', ['chave'])


def downgrade() -> None:
    # Drop constraints and table
    op.drop_constraint('uq_api_keys_chave', 'api_keys', type_='unique')
    op.drop_index('ix_api_keys_expires_em', 'api_keys')
    op.drop_index('ix_api_keys_criado_em', 'api_keys')
    op.drop_index('ix_api_keys_chave_ativo', 'api_keys')
    op.drop_table('api_keys')
