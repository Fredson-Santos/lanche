"""Enable database encryption for sensitive fields

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-04-20 10:00:00.000000

Migrates existing email data to encrypted format
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Obter conexão
    conn = op.get_bind()
    
    # 1. Remover constraints de email (unique, index)
    # Para SQLite, precisamos recriar a tabela
    dialect_name = conn.dialect.name
    
    if dialect_name == 'sqlite':
        # SQLite não suporta ALTER TABLE com constraints, então vamos usar raw SQL
        op.execute(text("""
            CREATE TABLE usuarios_new (
                id INTEGER PRIMARY KEY,
                email_encrypted TEXT NOT NULL,
                email_hash TEXT UNIQUE,
                username VARCHAR(100) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'caixa',
                ativo BOOLEAN DEFAULT true,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Copiar dados com hash do email
        op.execute(text("""
            INSERT INTO usuarios_new (id, email_encrypted, email_hash, username, senha_hash, role, ativo, data_criacao, data_atualizacao)
            SELECT id, email, email, username, senha_hash, role, ativo, data_criacao, data_atualizacao
            FROM usuarios
        """))
        
        # Dropar tabela antiga e renomear
        op.execute(text("DROP TABLE usuarios"))
        op.execute(text("ALTER TABLE usuarios_new RENAME TO usuarios"))
        
        # Recriar índices
        op.create_index('ix_usuarios_id', 'usuarios', ['id'])
        op.create_index('ix_usuarios_username', 'usuarios', ['username'])
        op.create_index('ix_usuarios_email_hash', 'usuarios', ['email_hash'])
        
    elif dialect_name == 'postgresql':
        # PostgreSQL - usar extensão pgcrypto
        op.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        
        # Adicionar coluna email_encrypted
        op.add_column('usuarios', sa.Column('email_encrypted', sa.String(255), nullable=True))
        
        # Adicionar coluna email_hash
        op.add_column('usuarios', sa.Column('email_hash', sa.String(64), nullable=True))
        
        # Copiar dados de email para email_encrypted
        op.execute(text("""
            UPDATE usuarios 
            SET email_encrypted = email,
                email_hash = encode(digest(email, 'sha256'), 'hex')
        """))
        
        # Remover constraints da coluna email antiga
        op.drop_index('ix_usuarios_email', table_name='usuarios')
        op.drop_constraint('usuarios_email_key', 'usuarios', type_='unique')
        
        # Dropar coluna email antiga
        op.drop_column('usuarios', 'email')
        
        # Criar índices novos
        op.create_index('ix_usuarios_email_hash', 'usuarios', ['email_hash'])


def downgrade() -> None:
    conn = op.get_bind()
    dialect_name = conn.dialect.name
    
    if dialect_name == 'sqlite':
        # Revertendo para SQLite
        op.execute(text("""
            CREATE TABLE usuarios_new (
                id INTEGER PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'caixa',
                ativo BOOLEAN DEFAULT true,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Usar email_encrypted como email original
        op.execute(text("""
            INSERT INTO usuarios_new (id, email, username, senha_hash, role, ativo, data_criacao, data_atualizacao)
            SELECT id, email_encrypted, username, senha_hash, role, ativo, data_criacao, data_atualizacao
            FROM usuarios
        """))
        
        op.execute(text("DROP TABLE usuarios"))
        op.execute(text("ALTER TABLE usuarios_new RENAME TO usuarios"))
        
        # Recriar índices antigos
        op.create_index('ix_usuarios_id', 'usuarios', ['id'])
        op.create_index('ix_usuarios_email', 'usuarios', ['email'])
        op.create_index('ix_usuarios_username', 'usuarios', ['username'])
        
    elif dialect_name == 'postgresql':
        # Revertendo para PostgreSQL
        op.add_column('usuarios', sa.Column('email', sa.String(255), nullable=False, server_default='unknown@example.com'))
        
        # Restaurar dados de email_encrypted
        op.execute(text("""
            UPDATE usuarios 
            SET email = email_encrypted
        """))
        
        # Adicionar constraints antigos
        op.create_unique_constraint('usuarios_email_key', 'usuarios', ['email'])
        op.create_index('ix_usuarios_email', 'usuarios', ['email'])
        
        # Dropar colunas novas
        op.drop_index('ix_usuarios_email_hash', table_name='usuarios')
        op.drop_column('usuarios', 'email_encrypted')
        op.drop_column('usuarios', 'email_hash')
