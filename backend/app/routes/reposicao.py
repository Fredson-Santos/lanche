"""
Rotas de gerenciamento de reposição automática - RF-06
GET /api/reposicao/ - Listar ordens
POST /api/reposicao/ - Criar ordem manual
PUT /api/reposicao/{id}/confirmar - Confirmar
PUT /api/reposicao/{id}/receber - Receber
DELETE /api/reposicao/{id} - Cancelar
"""

from typing import Annotated, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_gerente
from app.db.database import get_db
from app.models.ordem_reposicao import OrdemReposicao
from app.schemas.ordem_reposicao import (
    OrdemReposicaoCreate,
    OrdemReposicaoUpdate,
    OrdemReposicaoResponse,
    OrdemReposicaoListResponse,
)
from app.schemas.usuario import UsuarioResponse
from app.utils.reposicao import (
    criar_ordem_reposicao_manual,
    confirmar_ordem_reposicao,
    receber_ordem_reposicao,
    cancelar_ordem_reposicao,
    obter_ordens_pendentes,
    obter_ordens_recebidas_recentemente,
)
from app.core.logging import audit_logger as logger

router = APIRouter()


@router.get("/", response_model=List[OrdemReposicaoListResponse])
async def listar_ordens_reposicao(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
    status_filtro: str | None = None,
    estoque_id: int | None = None,
):
    """
    Lista ordens de reposição.
    
    - Usuários gerente/admin podem visualizar todas as ordens
    - Parâmetro `status_filtro` filtra por status (pendente, confirmada, recebida, cancelada)
    - Parâmetro `estoque_id` filtra por estoque específico
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        status_filtro: Filtro por status (opcional)
        estoque_id: Filtro por estoque (opcional)
        
    Returns:
        Lista de ordens de reposição
    """
    query = db.query(OrdemReposicao)
    
    if status_filtro:
        query = query.filter(OrdemReposicao.status == status_filtro)
    
    if estoque_id:
        query = query.filter(OrdemReposicao.estoque_id == estoque_id)
    
    ordens = query.order_by(OrdemReposicao.data_criacao.desc()).all()
    
    logger.info(f"Usuário {current_user.id} listou {len(ordens)} ordens de reposição")
    
    return ordens


@router.get("/{ordem_id}", response_model=OrdemReposicaoResponse)
async def obter_ordem_reposicao(
    ordem_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Obtém detalhes de uma ordem de reposição.
    
    Args:
        ordem_id: ID da ordem
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Ordem com detalhes completos
        
    Raises:
        HTTPException: Se ordem não encontrada
    """
    ordem = db.query(OrdemReposicao).filter(OrdemReposicao.id == ordem_id).first()
    
    if not ordem:
        logger.warning(f"Tentativa de acessar ordem de reposição inexistente: {ordem_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de reposição não encontrada"
        )
    
    logger.info(f"Usuário {current_user.id} visualizou ordem {ordem_id}")
    
    return ordem


@router.post("/", response_model=OrdemReposicaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_ordem_reposicao(
    ordem_data: OrdemReposicaoCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Cria uma ordem de reposição manual.
    
    Args:
        ordem_data: Dados da ordem de reposição
        db: Sessão do banco de dados
        current_user: Usuário autenticado (gerente/admin)
        
    Returns:
        Ordem criada
        
    Raises:
        HTTPException: Se estoque não existe
    """
    ordem = criar_ordem_reposicao_manual(
        db,
        ordem_data.estoque_id,
        ordem_data.produto_id,
        ordem_data.quantidade_solicitada,
        ordem_data.observacoes
    )
    
    if not ordem:
        logger.warning(f"Falha ao criar ordem de reposição para estoque {ordem_data.estoque_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado"
        )
    
    logger.info(f"Usuário {current_user.id} criou ordem de reposição {ordem.id}")
    
    return ordem


@router.put("/{ordem_id}/confirmar", response_model=OrdemReposicaoResponse)
async def confirmar_ordem(
    ordem_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Confirma uma ordem de reposição.
    
    Args:
        ordem_id: ID da ordem
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Ordem confirmada
        
    Raises:
        HTTPException: Se ordem não encontrada ou não está pendente
    """
    ordem = confirmar_ordem_reposicao(db, ordem_id)
    
    if not ordem:
        logger.warning(f"Falha ao confirmar ordem {ordem_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ordem não encontrada ou não está pendente"
        )
    
    logger.info(f"Usuário {current_user.id} confirmou ordem {ordem_id}")
    
    return ordem


@router.put("/{ordem_id}/receber", response_model=OrdemReposicaoResponse)
async def receber_ordem(
    ordem_id: int,
    quantidade_recebida: int = 0,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Registra o recebimento de uma ordem de reposição.
    
    Args:
        ordem_id: ID da ordem
        quantidade_recebida: Quantidade recebida
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Ordem atualizada
        
    Raises:
        HTTPException: Se ordem não encontrada ou cancelada
    """
    # Se quantidade não foi informada, usa a quantidade solicitada
    ordem = db.query(OrdemReposicao).filter(OrdemReposicao.id == ordem_id).first()
    
    if not ordem:
        logger.warning(f"Ordem de reposição não encontrada: {ordem_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem não encontrada"
        )
    
    if quantidade_recebida == 0:
        quantidade_recebida = ordem.quantidade_solicitada
    
    ordem_atualizada = receber_ordem_reposicao(db, ordem_id, quantidade_recebida)
    
    if not ordem_atualizada:
        logger.warning(f"Falha ao receber ordem {ordem_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ordem cancelada ou não pode ser recebida"
        )
    
    logger.info(f"Usuário {current_user.id} registrou recebimento da ordem {ordem_id}")
    
    return ordem_atualizada


@router.delete("/{ordem_id}", response_model=OrdemReposicaoResponse)
async def cancelar_ordem(
    ordem_id: int,
    motivo: str | None = None,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Cancela uma ordem de reposição.
    
    Args:
        ordem_id: ID da ordem
        motivo: Motivo do cancelamento
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Ordem cancelada
        
    Raises:
        HTTPException: Se ordem não encontrada ou já foi recebida
    """
    ordem = cancelar_ordem_reposicao(db, ordem_id, motivo)
    
    if not ordem:
        logger.warning(f"Falha ao cancelar ordem {ordem_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ordem não encontrada ou já foi recebida"
        )
    
    logger.info(f"Usuário {current_user.id} cancelou ordem {ordem_id}")
    
    return ordem


@router.get("/dashboard/resumo", response_model=dict)
async def obter_resumo_reposicoes(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_gerente)] = None,
):
    """
    Obtém resumo das ordens de reposição para o dashboard.
    
    Retorna:
        - Total de ordens pendentes/confirmadas
        - Total de ordens recebidas (últimos 7 dias)
        - Valor total de reposições
        
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Resumo de reposições
    """
    ordens_pendentes = obter_ordens_pendentes(db)
    ordens_recebidas = obter_ordens_recebidas_recentemente(db, dias=7)
    
    total_pendente = sum(o.quantidade_solicitada - o.quantidade_recebida for o in ordens_pendentes)
    total_recebido = sum(o.quantidade_recebida for o in ordens_recebidas)
    
    logger.info(f"Usuário {current_user.id} visualizou resumo de reposições")
    
    return {
        "ordens_pendentes": len(ordens_pendentes),
        "ordens_recebidas_7dias": len(ordens_recebidas),
        "quantidade_total_pendente": total_pendente,
        "quantidade_total_recebida": total_recebido,
    }
