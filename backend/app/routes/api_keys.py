"""
Rotas de API Keys para terceiros - RF-11
Endpoints para gerenciar chaves de acesso de delivery, parceiros, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.core.logging import audit_logger as logger
from app.models.api_key import APIKey
from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyUpdate,
    APIKeyResponse,
    APIKeyListResponse,
    APIKeyCreateResponse,
)
from app.utils.api_keys import (
    criar_api_key,
    verificar_api_key,
    revogar_api_key,
    obter_todas_api_keys,
)

router = APIRouter()


@router.post(
    "/",
    response_model=APIKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova API Key",
    description="Cria uma nova chave de API para terceiros (delivery, parceiros, etc.)"
)
async def criar_chave(
    payload: APIKeyCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Cria uma nova API Key com limite de requisições e expiração configuráveis.
    
    - **descricao**: Descrição clara (ex: "Delivery A", "Parceiro Logístico B")
    - **limite_requisicoes**: Máximo de requisições por janela (default: 100)
    - **janela_tempo**: Duração da janela em minutos (default: 60)
    - **expires_em**: Data de expiração (opcional)
    
    ⚠️ A chave é mostrada apenas uma vez nesta resposta. Guarde com segurança!
    """
    try:
        nova_chave = criar_api_key(
            db=db,
            descricao=payload.descricao,
            limite_requisicoes=payload.limite_requisicoes,
            janela_tempo=payload.janela_tempo,
            expires_em=payload.expires_em,
        )
        
        if not nova_chave:
            logger.error("Erro ao criar API Key")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar chave de API"
            )
        
        logger.info(f"API Key criada com sucesso: {nova_chave.chave[:8]}...")
        
        return APIKeyCreateResponse(
            id=nova_chave.id,
            chave=nova_chave.chave,
            ativo=nova_chave.ativo,
            descricao=nova_chave.descricao,
            criado_em=nova_chave.criado_em,
            message="⚠️ Guarde esta chave com segurança. Ela não será mostrada novamente!"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao criar API Key: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.get(
    "/",
    response_model=list[APIKeyListResponse],
    summary="Listar todas as API Keys",
    description="Lista todas as chaves de API (mostra apenas primeiros caracteres por segurança)"
)
async def listar_chaves(
    apenas_ativas: bool = True,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Lista todas as API Keys criadas.
    
    - **apenas_ativas**: Se True, retorna apenas chaves ativas (default: True)
    
    Note: Chaves são mascaradas por segurança. Use PUT /revoke para desativar.
    """
    try:
        chaves = obter_todas_api_keys(db=db, apenas_ativas=apenas_ativas)
        
        # Mascarar chaves por segurança (mostrar apenas primeiros 8 + últimos 4)
        response = []
        for chave in chaves:
            mascarada = f"{chave.chave[:8]}...{chave.chave[-4:]}"
            response.append(
                APIKeyListResponse(
                    id=chave.id,
                    chave=mascarada,
                    ativo=chave.ativo,
                    descricao=chave.descricao,
                    criado_em=chave.criado_em,
                    expires_em=chave.expires_em,
                    ultima_uso=chave.ultima_uso,
                )
            )
        
        logger.info(f"Listagem de {len(response)} API Keys")
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao listar API Keys: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar chaves de API"
        )


@router.get(
    "/{chave_id}",
    response_model=APIKeyResponse,
    summary="Obter detalhes de uma API Key",
    description="Obtém informações detalhadas de uma chave específica"
)
async def obter_chave(
    chave_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Retorna informações detalhadas de uma chave de API específica.
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            audit_logger.warning(f"Tentativa de acessar chave inexistente: {chave_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chave de API não encontrada"
            )
        
        return APIKeyResponse.from_orm(api_key)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter API Key: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter chave de API"
        )


@router.put(
    "/{chave_id}",
    response_model=APIKeyResponse,
    summary="Atualizar API Key",
    description="Atualiza limite, expiração ou status de uma chave"
)
async def atualizar_chave(
    chave_id: int,
    payload: APIKeyUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Atualiza os parâmetros de uma chave de API.
    
    - **ativo**: Ativa/desativa a chave
    - **descricao**: Nova descrição
    - **limite_requisicoes**: Novo limite
    - **expires_em**: Nova data de expiração
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chave de API não encontrada"
            )
        
        # Atualizar apenas os campos fornecidos
        if payload.ativo is not None:
            api_key.ativo = payload.ativo
        if payload.descricao is not None:
            api_key.descricao = payload.descricao
        if payload.limite_requisicoes is not None:
            api_key.limite_requisicoes = payload.limite_requisicoes
        if payload.expires_em is not None:
            api_key.expires_em = payload.expires_em
        
        db.commit()
        db.refresh(api_key)
        
        logger.info(f"API Key atualizada: {api_key.chave[:8]}...")
        
        return APIKeyResponse.from_orm(api_key)
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar API Key: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar chave de API"
        )


@router.delete(
    "/{chave_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revogar API Key",
    description="Remove permanentemente uma chave de API do sistema"
)
async def revogar_chave(
    chave_id: int,
    motivo: str = "Revogação administrativa",
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Exclui permanentemente uma chave de API, interrompendo qualquer acesso futuro.
    
    - **motivo**: Motivo da exclusão (opcional)
    
    A ação é irreversível. Se precisar apenas pausar o acesso, use o endpoint de atualização (ativo=false).
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chave de API não encontrada"
            )
        
        sucesso = revogar_api_key(db=db, chave_id=chave_id, motivo=motivo)
        
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao revogar chave"
            )
        
        audit_logger.info(f"API Key revogada: {api_key.chave[:8]}... (motivo: {motivo})")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao revogar API Key: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao revogar chave de API"
        )


@router.get(
    "/stats/resumo",
    summary="Resumo de estatísticas de API Keys",
    description="Retorna estatísticas gerais sobre uso de API Keys"
)
async def obter_resumo_stats(
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """
    Retorna um resumo de estatísticas sobre as chaves de API.
    """
    try:
        total_chaves = db.query(APIKey).count()
        chaves_ativas = db.query(APIKey).filter(APIKey.ativo == True).count()
        chaves_revogadas = total_chaves - chaves_ativas
        
        # Chaves com mais requisições usadas
        top_chaves = db.query(APIKey).order_by(
            APIKey.requisicoes_usadas.desc()
        ).limit(5).all()
        
        audit_logger.info(f"Resumo de stats de API Keys requisitado")
        
        return {
            "total_chaves": total_chaves,
            "chaves_ativas": chaves_ativas,
            "chaves_revogadas": chaves_revogadas,
            "top_5_mais_usadas": [
                {
                    "descricao": chave.descricao,
                    "requisicoes_usadas": chave.requisicoes_usadas,
                    "ultima_uso": chave.ultima_uso,
                }
                for chave in top_chaves
            ]
        }
    
    except Exception as e:
        logger.error(f"Erro ao gerar resumo de stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar estatísticas"
        )
