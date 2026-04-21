"""
Rotas de gerenciamento de usuários - CRUD de usuários (apenas admin)
"""

import hashlib
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.security import hash_password
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter()


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(
    usuario_data: UsuarioCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_admin)] = None,
):
    """
    Cria um novo usuário (apenas admin).

    Args:
        usuario_data: Dados do usuário a criar
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role admin

    Returns:
        Usuário criado

    Raises:
        HTTPException: Se o email já estiver registrado
    """
    # Verifica se o email já existe (usando email_hash)
    # Email é um campo encriptado, então precisa comparar hashes
    email_hash = hashlib.sha256(usuario_data.email.encode()).hexdigest()
    db_usuario = db.query(Usuario).filter(Usuario.email_hash == email_hash).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado",
        )

    # Verifica se o username já existe
    db_usuario = db.query(Usuario).filter(Usuario.username == usuario_data.username).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já registrado",
        )

    # Cria novo usuário
    novo_usuario = Usuario(
        email=usuario_data.email,
        username=usuario_data.username,
        senha_hash=hash_password(usuario_data.senha),
        role=usuario_data.role,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return UsuarioResponse.from_orm(novo_usuario)


@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_admin)] = None,
):
    """
    Lista todos os usuários (apenas admin).

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role admin

    Returns:
        Lista de usuários
    """
    usuarios = db.query(Usuario).all()
    return [UsuarioResponse.from_orm(u) for u in usuarios]


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obter_usuario(
    usuario_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_admin)] = None,
):
    """
    Obtém dados de um usuário específico (apenas admin).

    Args:
        usuario_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role admin

    Returns:
        Dados do usuário

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return UsuarioResponse.from_orm(usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_admin)] = None,
):
    """
    Atualiza dados de um usuário (apenas admin).

    Args:
        usuario_id: ID do usuário a atualizar
        usuario_data: Dados a atualizar
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role admin

    Returns:
        Usuário atualizado

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    # Atualiza apenas os campos fornecidos
    if usuario_data.email is not None:
        # Verifica se o email já está em uso (usando email_hash)
        # Email é um campo encriptado, então precisa comparar hashes
        email_hash = hashlib.sha256(usuario_data.email.encode()).hexdigest()
        db_usuario = (
            db.query(Usuario)
            .filter(Usuario.email_hash == email_hash, Usuario.id != usuario_id)
            .first()
        )
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado",
            )
        usuario.email = usuario_data.email
        usuario.email_hash = email_hash  # Atualiza o hash também

    if usuario_data.username is not None:
        # Verifica se o username já está em uso
        db_usuario = (
            db.query(Usuario)
            .filter(Usuario.username == usuario_data.username, Usuario.id != usuario_id)
            .first()
        )
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já registrado",
            )
        usuario.username = usuario_data.username

    if usuario_data.role is not None:
        usuario.role = usuario_data.role

    if usuario_data.ativo is not None:
        usuario.ativo = usuario_data.ativo

    db.commit()
    db.refresh(usuario)

    return UsuarioResponse.from_orm(usuario)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(
    usuario_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_admin)] = None,
):
    """
    Deleta um usuário (apenas admin).

    Args:
        usuario_id: ID do usuário a deletar
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role admin

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    db.delete(usuario)
    db.commit()
