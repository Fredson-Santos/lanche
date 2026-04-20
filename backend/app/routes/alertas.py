"""
Rotas de gerenciamento de alertas - RF-01, RF-02, RF-03
GET /api/alertas/ - Listar alertas ativos
PUT /api/alertas/{id} - Marcar alerta como lido
"""

from typing import Annotated, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_vendedor
from app.db.database import get_db
from app.models.alerta import Alerta
from app.schemas.alerta import AlertaResponse, AlertaListResponse, AlertaUpdate
from app.schemas.usuario import UsuarioResponse
from app.utils.alertas import (
    marcar_alerta_como_lido,
    limpar_alertas_resolvidos,
    obter_alertas_ativos,
)
from app.core.logging import audit_logger

router = APIRouter()


@router.get("/dashboard/resumo", response_model=dict)
async def obter_resumo_alertas(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_vendedor)] = None,
):
    """
    Obtém resumo dos alertas para o dashboard.
    
    Retorna:
        - Total de alertas ativos
        - Alertas por tipo
        - Produtos com alertas
        
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Resumo de alertas
    """
    alertas_ativos = db.query(Alerta).filter(
        Alerta.ativo == True,
        Alerta.lido == False
    ).all()
    
    # Agrupa alertas por tipo
    alertas_por_tipo = {}
    for alerta in alertas_ativos:
        tipo = alerta.tipo
        alertas_por_tipo[tipo] = alertas_por_tipo.get(tipo, 0) + 1
    
    # Conta produtos com alertas
    produtos_com_alertas = len(set(a.produto_id for a in alertas_ativos))
    
    logger.info(f"Usuário {current_user.id} visualizou resumo de alertas")
    
    return {
        "total_alertas": len(alertas_ativos),
        "alertas_por_tipo": alertas_por_tipo,
        "produtos_com_alertas": produtos_com_alertas,
    }


@router.get("/", response_model=List[AlertaListResponse])
async def listar_alertas(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_vendedor)] = None,
    apenas_ativos: bool = True,
    produto_id: int | None = None,
):
    """
    Lista alertas do sistema.
    
    - Usuários vendedor/gerente/admin podem visualizar todos os alertas
    - Parâmetro `apenas_ativos=true` mostra apenas alertas não lidos
    - Parâmetro `produto_id` filtra alertas de um produto específico
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        apenas_ativos: Se True, mostra apenas alertas não lidos e ativos
        produto_id: ID do produto para filtrar (opcional)
        
    Returns:
        Lista de alertas
    """
    query = db.query(Alerta)
    
    if apenas_ativos:
        query = query.filter(Alerta.ativo == True, Alerta.lido == False)
    
    if produto_id:
        query = query.filter(Alerta.produto_id == produto_id)
    
    alertas = query.order_by(Alerta.data_criacao.desc()).all()
    
    logger.info(f"Usuário {current_user.id} listou {len(alertas)} alertas")
    
    return alertas


@router.get("/{alerta_id}", response_model=AlertaResponse)
async def obter_alerta(
    alerta_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_vendedor)] = None,
):
    """
    Obtém detalhes de um alerta específico.
    
    Args:
        alerta_id: ID do alerta
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Alerta com detalhes completos
        
    Raises:
        HTTPException: Se alerta não encontrado
    """
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    
    if not alerta:
        logger.warning(f"Tentativa de acessar alerta {alerta_id} inexistente")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta não encontrado"
        )
    
    logger.info(f"Usuário {current_user.id} visualizou alerta {alerta_id}")
    
    return alerta


@router.put("/{alerta_id}", response_model=AlertaResponse)
async def marcar_alerta_lido(
    alerta_id: int,
    alerta_data: AlertaUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UsuarioResponse, Depends(require_vendedor)] = None,
):
    """
    Marca um alerta como lido ou resolve ele.
    
    Args:
        alerta_id: ID do alerta
        alerta_data: Dados de atualização (lido, ativo)
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Alerta atualizado
        
    Raises:
        HTTPException: Se alerta não encontrado
    """
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    
    if not alerta:
        logger.warning(f"Tentativa de atualizar alerta {alerta_id} inexistente")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta não encontrado"
        )
    
    # Atualiza campos fornecidos
    if alerta_data.lido is not None:
        alerta.lido = alerta_data.lido
        if alerta_data.lido:
            alerta.data_leitura = datetime.now(tz=datetime.now().astimezone().tzinfo)
    
    if alerta_data.ativo is not None:
        alerta.ativo = alerta_data.ativo
        if not alerta_data.ativo:  # Resolvido
            alerta.data_resolucao = datetime.now(tz=datetime.now().astimezone().tzinfo)
    
    db.commit()
    db.refresh(alerta)
    
    logger.info(f"Usuário {current_user.id} atualizou alerta {alerta_id}")
    
    return alerta
