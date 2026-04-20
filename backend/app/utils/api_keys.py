"""
Utilitários para gerenciamento de API Keys - RF-11
Funções para gerar, verificar, validar e gerenciar chaves de terceiros
"""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.core.logging import audit_logger


def gerar_chave_api() -> str:
    """
    Gera uma nova chave de API usando UUID v4
    
    Returns:
        str: Chave em formato hex (32 caracteres)
    """
    return uuid.uuid4().hex


def criar_api_key(
    db: Session,
    descricao: str,
    limite_requisicoes: int = 100,
    janela_tempo: int = 60,
    expires_em: datetime | None = None,
) -> APIKey | None:
    """
    Cria uma nova API key no banco de dados
    
    Args:
        db: Sessão do banco de dados
        descricao: Descrição da chave
        limite_requisicoes: Limite de requisições na janela
        janela_tempo: Duração da janela em minutos
        expires_em: Data de expiração (opcional)
    
    Returns:
        APIKey: Chave criada, ou None se erro
    """
    try:
        chave = gerar_chave_api()
        
        nova_chave = APIKey(
            chave=chave,
            ativo=True,
            limite_requisicoes=limite_requisicoes,
            janela_tempo=janela_tempo,
            expires_em=expires_em,
            descricao=descricao,
        )
        
        db.add(nova_chave)
        db.commit()
        db.refresh(nova_chave)
        
        audit_logger.info(
            f"API Key criada: {chave[:8]}... (descrição: {descricao})",
            event="api_key_created",
            chave_id=nova_chave.id
        )
        
        return nova_chave
    
    except Exception as e:
        db.rollback()
        audit_logger.error(f"Erro ao criar API Key: {str(e)}")
        return None


def verificar_api_key(db: Session, chave: str) -> APIKey | None:
    """
    Verifica se uma chave de API é válida e ativa
    
    Args:
        db: Sessão do banco de dados
        chave: Chave a verificar
    
    Returns:
        APIKey: Objeto da chave se válida, None se inválida
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.chave == chave).first()
        
        if not api_key:
            audit_logger.warning(f"Tentativa de acesso com chave inexistente: {chave[:8]}...")
            return None
        
        if not api_key.esta_ativa():
            audit_logger.warning(f"Tentativa de acesso com chave inativa: {chave[:8]}...")
            return None
        
        return api_key
    
    except Exception as e:
        audit_logger.error(f"Erro ao verificar API Key: {str(e)}")
        return None


def registrar_uso_api_key(db: Session, chave_id: int) -> bool:
    """
    Registra um uso de API key (incrementa contador e atualiza last used)
    
    Args:
        db: Sessão do banco de dados
        chave_id: ID da chave
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            return False
        
        api_key.ultima_uso = datetime.utcnow()
        api_key.requisicoes_usadas += 1
        
        db.commit()
        
        return True
    
    except Exception as e:
        db.rollback()
        audit_logger.error(f"Erro ao registrar uso de API Key: {str(e)}")
        return False


def verificar_rate_limit(db: Session, chave_id: int) -> bool:
    """
    Verifica se a chave atingiu seu limite de requisições
    
    Args:
        db: Sessão do banco de dados
        chave_id: ID da chave
    
    Returns:
        bool: True se dentro do limite, False se excedeu
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            return False
        
        if api_key.requisicoes_usadas >= api_key.limite_requisicoes:
            audit_logger.warning(
                f"Rate limit excedido para chave {api_key.chave[:8]}... "
                f"({api_key.requisicoes_usadas}/{api_key.limite_requisicoes})"
            )
            return False
        
        return True
    
    except Exception as e:
        audit_logger.error(f"Erro ao verificar rate limit: {str(e)}")
        return False


def resetar_contador_requisicoes(db: Session, chave_id: int) -> bool:
    """
    Reseta o contador de requisições da chave (normalmente chamado em job agendado)
    
    Args:
        db: Sessão do banco de dados
        chave_id: ID da chave
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            return False
        
        api_key.requisicoes_usadas = 0
        db.commit()
        
        audit_logger.info(f"Contador de requisições resetado para chave {api_key.chave[:8]}...")
        
        return True
    
    except Exception as e:
        db.rollback()
        audit_logger.error(f"Erro ao resetar contador: {str(e)}")
        return False


def revogar_api_key(db: Session, chave_id: int, motivo: str | None = None) -> bool:
    """
    Revoga (desativa) uma chave de API
    
    Args:
        db: Sessão do banco de dados
        chave_id: ID da chave
        motivo: Motivo da revogação (opcional)
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        api_key = db.query(APIKey).filter(APIKey.id == chave_id).first()
        
        if not api_key:
            return False
        
        api_key.ativo = False
        db.commit()
        
        audit_logger.info(
            f"API Key revogada: {api_key.chave[:8]}... (motivo: {motivo or 'não especificado'})",
            event="api_key_revoked",
            chave_id=chave_id
        )
        
        return True
    
    except Exception as e:
        db.rollback()
        audit_logger.error(f"Erro ao revogar API Key: {str(e)}")
        return False


def obter_todas_api_keys(db: Session, apenas_ativas: bool = False) -> list[APIKey]:
    """
    Obtém todas as API keys
    
    Args:
        db: Sessão do banco de dados
        apenas_ativas: Se True, retorna apenas chaves ativas
    
    Returns:
        list: Lista de APIKey
    """
    query = db.query(APIKey)
    
    if apenas_ativas:
        query = query.filter(APIKey.ativo == True)
    
    return query.order_by(APIKey.criado_em.desc()).all()


def limpar_api_keys_expiradas(db: Session) -> int:
    """
    Remove (soft delete) API keys que expiraram há mais de 30 dias
    Job agendado para executar periodicamente
    
    Args:
        db: Sessão do banco de dados
    
    Returns:
        int: Número de chaves limpas
    """
    try:
        dias_retencao = 30
        data_limite = datetime.utcnow() - timedelta(days=dias_retencao)
        
        # Encontra chaves expiradas e inativas
        chaves_expiradas = db.query(APIKey).filter(
            APIKey.ativo == False,
            APIKey.expires_em < data_limite
        ).all()
        
        contador = 0
        for chave in chaves_expiradas:
            db.delete(chave)
            contador += 1
        
        db.commit()
        
        audit_logger.info(f"Limpeza de API Keys: {contador} chaves removidas")
        
        return contador
    
    except Exception as e:
        db.rollback()
        audit_logger.error(f"Erro ao limpar API Keys expiradas: {str(e)}")
        return 0
