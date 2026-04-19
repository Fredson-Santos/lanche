"""
Dependências do FastAPI para autenticação e autorização
Fornece funções para validação de JWT e controle de acesso baseado em role (RBAC)
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Cria um token JWT com os dados fornecidos.

    Args:
        data: Dicionário com dados a serem incluídos no token
        expires_delta: Tempo de expiração customizado (opcional)

    Returns:
        Token JWT assinado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> UsuarioResponse:
    """
    Extrai e valida o usuário a partir do token JWT.

    Args:
        token: Token JWT obtido do header Authorization
        db: Sessão do banco de dados

    Returns:
        Usuário validado

    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception

    return UsuarioResponse.from_orm(usuario)


async def get_current_active_user(
    current_user: Annotated[UsuarioResponse, Depends(get_current_user)],
) -> UsuarioResponse:
    """
    Verifica se o usuário está ativo.

    Args:
        current_user: Usuário obtido do token JWT

    Returns:
        Usuário se estiver ativo

    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    if not current_user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


def require_role(*allowed_roles: str):
    """
    Factory que retorna uma dependência para validar o role do usuário.

    Args:
        *allowed_roles: Roles permitidas (ex: "admin", "gerente", "caixa")

    Returns:
        Dependência que valida se o usuário tem permissão
    """

    async def check_role(
        current_user: Annotated[UsuarioResponse, Depends(get_current_active_user)]
    ) -> UsuarioResponse:
        """Valida se o usuário tem um dos roles permitidos"""
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' não tem permissão para acessar este recurso",
            )
        return current_user

    return check_role


# Dependências pré-configuradas para roles comuns
require_admin = require_role("admin")
require_gerente = require_role("admin", "gerente")
require_caixa = require_role("admin", "gerente", "caixa")
