"""
Rotas de gerenciamento de estoque
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_gerente
from app.db.database import get_db
from app.models.estoque import Estoque
from app.schemas.estoque import EstoqueResponse, EstoqueUpdate
from app.schemas.usuario import UsuarioResponse

router = APIRouter()


@router.get("/", response_model=List[EstoqueResponse])
async def listar_estoque(
    db: Annotated[Session, Depends(get_db)],
):
    """
    Lista todo o estoque de produtos (público).

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de estoque
    """
    estoque = db.query(Estoque).all()
    return [EstoqueResponse.from_orm(e) for e in estoque]


@router.get("/{produto_id}", response_model=EstoqueResponse)
async def obter_estoque_produto(
    produto_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Obtém estoque de um produto específico (público).

    Args:
        produto_id: ID do produto
        db: Sessão do banco de dados

    Returns:
        Dados de estoque

    Raises:
        HTTPException: Se o produto não tiver estoque registrado
    """
    estoque = db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado para este produto",
        )

    return EstoqueResponse.from_orm(estoque)


@router.put("/{produto_id}", response_model=EstoqueResponse)
async def atualizar_estoque(
    produto_id: int,
    estoque_data: EstoqueUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Atualiza a quantidade de estoque de um produto (gerente ou admin).

    Args:
        produto_id: ID do produto
        estoque_data: Nova quantidade
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Estoque atualizado

    Raises:
        HTTPException: Se o estoque não for encontrado
    """
    estoque = db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado",
        )

    if estoque_data.quantidade < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantidade não pode ser negativa",
        )

    estoque.quantidade = estoque_data.quantidade
    db.commit()
    db.refresh(estoque)

    return EstoqueResponse.from_orm(estoque)
