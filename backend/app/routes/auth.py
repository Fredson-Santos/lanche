"""
Rotas de autenticação - Login e gerenciamento de tokens JWT
"""

import hashlib
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import create_access_token
from app.core.security import verify_password
from app.core.config import settings
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UsuarioLogin,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Endpoint de login - Autentica o usuário e retorna um token JWT.

    Args:
        login_data: Email e senha do usuário
        db: Sessão do banco de dados

    Returns:
        Token JWT e dados do usuário

    Raises:
        HTTPException: Se email ou senha forem inválidos
    """
    # Busca o usuário pelo email_hash (SHA-256 do email)
    # Necessário porque email é um campo encriptado no banco de dados
    email_hash = hashlib.sha256(login_data.email.encode()).hexdigest()
    usuario = db.query(Usuario).filter(Usuario.email_hash == email_hash).first()

    # Valida se o usuário existe e a senha está correta
    if not usuario or not verify_password(login_data.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    # Valida se o usuário está ativo
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )

    # Cria o token com o email do usuário como identificador
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        usuario={
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "role": usuario.role,
            "ativo": usuario.ativo,
            "data_criacao": usuario.data_criacao,
            "data_atualizacao": usuario.data_atualizacao,
        },
    )
