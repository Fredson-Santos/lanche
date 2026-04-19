"""
Rotas de relatórios e analytics
"""

from typing import Annotated
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import require_gerente
from app.db.database import get_db
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.schemas.usuario import UsuarioResponse

router = APIRouter()


@router.get("/vendas/total")
async def relatorio_total_vendas(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna o total de vendas agregado (gerente ou admin).

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Total de vendas em reais
    """
    total = db.query(func.sum(Venda.total)).scalar() or 0
    return {"total_vendas": float(total)}


@router.get("/vendas/por-periodo")
async def relatorio_vendas_periodo(
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna vendas em um período específico (gerente ou admin).

    Args:
        data_inicio: Data de início do período
        data_fim: Data de fim do período
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Total de vendas no período
    """
    vendas = (
        db.query(func.sum(Venda.total))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao <= data_fim)
        .scalar()
        or 0
    )
    return {
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat(),
        },
        "total_vendas": float(vendas),
    }


@router.get("/produtos/mais-vendidos")
async def relatorio_produtos_mais_vendidos(
    limite: int = Query(10, ge=1, le=100),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna os produtos mais vendidos (gerente ou admin).

    Args:
        limite: Quantidade máxima de produtos a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Lista dos produtos mais vendidos com quantidade total vendida
    """
    produtos_vendidos = (
        db.query(
            ItemVenda.produto_id,
            func.sum(ItemVenda.quantidade).label("total_vendido"),
        )
        .group_by(ItemVenda.produto_id)
        .order_by(func.sum(ItemVenda.quantidade).desc())
        .limit(limite)
        .all()
    )

    resultado = [
        {"produto_id": p[0], "quantidade_vendida": p[1]} for p in produtos_vendidos
    ]
    return {"produtos_mais_vendidos": resultado}


@router.get("/vendas/quantidade-por-dia")
async def relatorio_quantidade_vendas_dia(
    data: datetime = Query(...),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna quantidade de vendas em um dia específico (gerente ou admin).

    Args:
        data: Data do relatório
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Quantidade e valor total de vendas no dia
    """
    data_inicio = data.replace(hour=0, minute=0, second=0, microsecond=0)
    data_fim = data_inicio + timedelta(days=1)

    quantidade = (
        db.query(func.count(Venda.id))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    total = (
        db.query(func.sum(Venda.total))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    return {
        "data": data.date().isoformat(),
        "quantidade_vendas": quantidade,
        "valor_total": float(total),
    }


@router.get("/vendas")
async def relatorio_vendas(
    inicio: str = Query(...),
    fim: str = Query(...),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna vendas em um período específico (gerente ou admin).

    Args:
        inicio: Data de início (formato YYYY-MM-DD)
        fim: Data de fim (formato YYYY-MM-DD)
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Total de vendas e quantidade no período
    """
    from datetime import datetime as dt
    data_inicio = dt.fromisoformat(inicio)
    data_fim = dt.fromisoformat(fim) + timedelta(days=1)

    quantidade = (
        db.query(func.count(Venda.id))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    total = (
        db.query(func.sum(Venda.total))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    return {
        "periodo": {
            "inicio": inicio,
            "fim": fim,
        },
        "quantidade_vendas": quantidade,
        "valor_total": float(total or 0),
    }


@router.get("/faturamento")
async def relatorio_faturamento(
    inicio: str = Query(...),
    fim: str = Query(...),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna o faturamento em um período específico (gerente ou admin).

    Args:
        inicio: Data de início (formato YYYY-MM-DD)
        fim: Data de fim (formato YYYY-MM-DD)
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Total de faturamento e valor médio por venda
    """
    from datetime import datetime as dt
    data_inicio = dt.fromisoformat(inicio)
    data_fim = dt.fromisoformat(fim) + timedelta(days=1)

    total_faturamento = (
        db.query(func.sum(Venda.total))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    quantidade_vendas = (
        db.query(func.count(Venda.id))
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .scalar()
        or 0
    )

    valor_medio = float(total_faturamento / quantidade_vendas) if quantidade_vendas > 0 else 0

    return {
        "periodo": {
            "inicio": inicio,
            "fim": fim,
        },
        "total_faturamento": float(total_faturamento or 0),
        "quantidade_vendas": quantidade_vendas,
        "valor_medio_venda": valor_medio,
    }


@router.get("/vendas-por-dia")
async def relatorio_vendas_por_dia(
    inicio: str = Query(...),
    fim: str = Query(...),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Retorna vendas agregadas por dia em um período específico (gerente ou admin).

    Args:
        inicio: Data de início (formato YYYY-MM-DD)
        fim: Data de fim (formato YYYY-MM-DD)
        db: Sessão do banco de dados
        current_user: Usuário autenticado com role gerente ou admin

    Returns:
        Lista de vendas por dia com quantidade e valor
    """
    from datetime import datetime as dt
    from sqlalchemy import func as sql_func
    
    data_inicio = dt.fromisoformat(inicio)
    data_fim = dt.fromisoformat(fim) + timedelta(days=1)

    vendas_por_dia = (
        db.query(
            sql_func.date(Venda.data_criacao).label("data"),
            sql_func.count(Venda.id).label("quantidade"),
            sql_func.sum(Venda.total).label("total"),
        )
        .filter(Venda.data_criacao >= data_inicio)
        .filter(Venda.data_criacao < data_fim)
        .group_by(sql_func.date(Venda.data_criacao))
        .order_by(sql_func.date(Venda.data_criacao))
        .all()
    )

    resultado = [
        {
            "data": str(dia[0]),
            "quantidade": dia[1],
            "total": float(dia[2] or 0),
        }
        for dia in vendas_por_dia
    ]

    return {
        "periodo": {
            "inicio": inicio,
            "fim": fim,
        },
        "vendas_por_dia": resultado,
    }
