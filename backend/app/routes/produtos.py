"""
Rotas de gerenciamento de produtos - CRUD de produtos
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_gerente
from app.db.database import get_db
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.schemas.usuario import UsuarioResponse

router = APIRouter()


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(
    produto_data: ProdutoCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Cria um novo produto (gerente ou admin).

    Args:
        produto_data: Dados do produto
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Produto criado
    """
    novo_produto = Produto(
        nome=produto_data.nome,
        descricao=produto_data.descricao,
        preco=produto_data.preco,
        categoria=produto_data.categoria,
        data_validade=produto_data.data_validade,
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    # Cria registro de estoque inicial
    estoque = Estoque(
        produto_id=novo_produto.id,
        quantidade=0,
    )
    db.add(estoque)
    db.commit()

    return ProdutoResponse.from_orm(novo_produto)


@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos(
    db: Annotated[Session, Depends(get_db)],
):
    """
    Lista todos os produtos (público).

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de produtos
    """
    produtos = db.query(Produto).all()
    return [ProdutoResponse.from_orm(p) for p in produtos]


@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(
    produto_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Obtém dados de um produto específico (público).

    Args:
        produto_id: ID do produto
        db: Sessão do banco de dados

    Returns:
        Dados do produto

    Raises:
        HTTPException: Se o produto não for encontrado
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    return ProdutoResponse.from_orm(produto)


@router.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int,
    produto_data: ProdutoUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Atualiza dados de um produto (gerente ou admin).

    Args:
        produto_id: ID do produto
        produto_data: Dados a atualizar
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Produto atualizado

    Raises:
        HTTPException: Se o produto não for encontrado
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    if produto_data.nome is not None:
        produto.nome = produto_data.nome
    if produto_data.descricao is not None:
        produto.descricao = produto_data.descricao
    if produto_data.preco is not None:
        produto.preco = produto_data.preco
    if produto_data.categoria is not None:
        produto.categoria = produto_data.categoria
    if produto_data.data_validade is not None:
        produto.data_validade = produto_data.data_validade

    db.commit()
    db.refresh(produto)

    return ProdutoResponse.from_orm(produto)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(
    produto_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Deleta um produto (gerente ou admin).

    Args:
        produto_id: ID do produto
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Raises:
        HTTPException: Se o produto não for encontrado
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    db.delete(produto)
    db.commit()
