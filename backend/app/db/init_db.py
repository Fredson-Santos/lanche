"""
Script de inicialização do banco de dados
Cria apenas o usuário admin na primeira execução
"""

from sqlalchemy.orm import Session

import hashlib
from app.core.security import hash_password
from app.models.usuario import Usuario


def init_db(db: Session) -> None:
    """
    Inicializa o banco de dados com o usuário admin na primeira execução.
    
    Args:
        db: Sessão do banco de dados
    """
    # Verifica se já existem usuários
    usuarios_count = db.query(Usuario).count()
    if usuarios_count > 0:
        return  # Banco já inicializado

    # Cria usuário admin padrão
    admin_email = "admin@admin.com"
    admin_user = Usuario(
        email=admin_email,
        email_hash=hashlib.sha256(admin_email.encode()).hexdigest(),
        username="admin",
        senha_hash=hash_password("Admin123"),
        role="admin",
        ativo=True,
    )
    
    db.add(admin_user)
    db.commit()
