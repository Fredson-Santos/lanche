"""
Rotas de gerenciamento de vendas
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_caixa, get_current_active_user
from app.db.database import get_db
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.estoque import Estoque
from app.models.produto import Produto
from app.schemas.venda import VendaCreate, VendaResponse, ItemVendaCreate
from app.schemas.usuario import UsuarioResponse

router = APIRouter()


@router.post("/", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
async def criar_venda(
    venda_data: VendaCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_caixa)],
):
    """
    Cria uma nova venda com itens e atualiza o estoque (caixa ou superior).

    Args:
        venda_data: Dados da venda com itens
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role caixa, gerente ou admin

    Returns:
        Venda criada com itens

    Raises:
        HTTPException: Se houver erro ao criar venda ou atualizar estoque
    """
    try:
        total_venda = 0
        for item_data in venda_data.itens:
            total_venda += item_data.preco_unitario * item_data.quantidade

        # Cria a venda
        nova_venda = Venda(
            usuario_id=current_user.id,
            total=total_venda,
        )
        db.add(nova_venda)
        db.flush()  # Agora o total > 0 atende à constraint

        # Cria itens da venda e atualiza estoque
        for item_data in venda_data.itens:
            # Obtém o produto para validar
            produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
            if not produto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto ID {item_data.produto_id} não encontrado",
                )

            # Obtém o estoque do produto
            estoque = (
                db.query(Estoque)
                .filter(Estoque.produto_id == item_data.produto_id)
                .first()
            )

            if not estoque:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Estoque não encontrado para produto ID {item_data.produto_id}",
                )

            # Verifica se há estoque suficiente
            if estoque.quantidade < item_data.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente para produto ID {item_data.produto_id}. Disponível: {estoque.quantidade}",
                )

            # Cria o item da venda
            item_venda = ItemVenda(
                venda_id=nova_venda.id,
                produto_id=item_data.produto_id,
                quantidade=item_data.quantidade,
                preco_unitario=item_data.preco_unitario,
            )
            db.add(item_venda)

            # Atualiza o estoque
            estoque.quantidade -= item_data.quantidade

        # Atualiza o total da venda (já calculado no inicio)
        nova_venda.total = total_venda

        db.commit()
        db.refresh(nova_venda)

        return VendaResponse.from_orm(nova_venda)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar venda: {str(e)}",
        )


@router.get("/", response_model=List[VendaResponse])
async def listar_vendas(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_caixa)],
):
    """
    Lista todas as vendas (caixa ou superior).

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role caixa, gerente ou admin

    Returns:
        Lista de vendas
    """
    vendas = db.query(Venda).all()
    return [VendaResponse.from_orm(v) for v in vendas]


@router.get("/{venda_id}", response_model=VendaResponse)
async def obter_venda(
    venda_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_caixa)],
):
    """
    Obtém dados de uma venda específica (caixa ou superior).

    Args:
        venda_id: ID da venda
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role caixa, gerente ou admin

    Returns:
        Dados da venda com itens

    Raises:
        HTTPException: Se a venda não for encontrada
    """
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada",
        )

    return VendaResponse.from_orm(venda)
