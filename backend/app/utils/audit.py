"""
Utilitários para Auditoria
Funções auxiliares para registrar eventos de auditoria
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.auditoria import AuditoriaLog
from app.core.logging import audit_logger


def registrar_evento_auditoria(
    db: Session,
    event_type: str,
    action: str,
    status: str = "SUCCESS",
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    error_message: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    http_method: Optional[str] = None,
    http_path: Optional[str] = None,
    http_status: Optional[int] = None,
    ip_address: Optional[str] = None,
) -> AuditoriaLog:
    """
    Registra um evento de auditoria no banco de dados e em logs estruturados
    
    Args:
        db: Sessão do banco de dados
        event_type: Tipo de evento (AUTH, CRUD, SECURITY, SYSTEM)
        action: Ação realizada
        status: Status do evento (SUCCESS, FAILURE, PARTIAL)
        user_id: ID do usuário (opcional)
        resource_type: Tipo de recurso afetado (opcional)
        resource_id: ID do recurso (opcional)
        error_message: Mensagem de erro (opcional)
        context: Contexto estruturado (opcional)
        http_method: Método HTTP (opcional)
        http_path: Caminho HTTP (opcional)
        http_status: Status HTTP (opcional)
        ip_address: Endereço IP (opcional)
    
    Returns:
        AuditoriaLog: Objeto do log criado
        
    Raises:
        Exception: Erros ao salvar no banco de dados
    """
    try:
        # Cria objeto de log
        log = AuditoriaLog(
            event_type=event_type,
            action=action,
            status=status,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            error_message=error_message,
            context=context,
            http_method=http_method,
            http_path=http_path,
            http_status=http_status,
            ip_address=ip_address,
            retencao_ativa=True,
        )
        
        # Salva no banco de dados
        db.add(log)
        db.commit()
        db.refresh(log)
        
        # Log estruturado em JSON
        audit_logger.log_event(
            event_type=event_type,
            action=action,
            status=status,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            error_message=error_message,
            details=context,
        )
        
        return log
        
    except Exception as e:
        db.rollback()
        # Log de erro
        audit_logger.error(
            f"Falha ao registrar auditoria: {event_type} - {action}",
            error=str(e),
        )
        raise


def registrar_login_bem_sucedido(
    db: Session,
    user_id: int,
    email: str,
    ip_address: Optional[str] = None,
) -> AuditoriaLog:
    """
    Registra um login bem-sucedido
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário
        email: Email do usuário
        ip_address: IP do cliente (opcional)
        
    Returns:
        AuditoriaLog: Log criado
    """
    return registrar_evento_auditoria(
        db=db,
        event_type="AUTH",
        action="LOGIN_SUCCESS",
        status="SUCCESS",
        user_id=user_id,
        resource_type="Usuario",
        resource_id=user_id,
        context={"email": email},
        ip_address=ip_address,
    )


def registrar_falha_login(
    db: Session,
    email: str,
    erro: str,
    ip_address: Optional[str] = None,
) -> AuditoriaLog:
    """
    Registra uma tentativa de login falhada
    
    Args:
        db: Sessão do banco de dados
        email: Email tentado
        erro: Motivo da falha
        ip_address: IP do cliente (opcional)
        
    Returns:
        AuditoriaLog: Log criado
    """
    return registrar_evento_auditoria(
        db=db,
        event_type="AUTH",
        action="LOGIN_FAILURE",
        status="FAILURE",
        resource_type="Usuario",
        error_message=erro,
        context={"email": email},
        ip_address=ip_address,
    )


def registrar_operacao_crud(
    db: Session,
    operacao: str,  # CREATE, READ, UPDATE, DELETE
    resource_type: str,
    resource_id: int,
    user_id: int,
    status: str = "SUCCESS",
    error_message: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> AuditoriaLog:
    """
    Registra uma operação CRUD
    
    Args:
        db: Sessão do banco de dados
        operacao: CREATE, READ, UPDATE, DELETE
        resource_type: Tipo de recurso
        resource_id: ID do recurso
        user_id: ID do usuário
        status: SUCCESS ou FAILURE
        error_message: Mensagem de erro se houver
        context: Contexto adicional
        ip_address: IP do cliente
        
    Returns:
        AuditoriaLog: Log criado
    """
    return registrar_evento_auditoria(
        db=db,
        event_type="CRUD",
        action=operacao,
        status=status,
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        error_message=error_message,
        context=context,
        ip_address=ip_address,
    )


def registrar_acesso_negado(
    db: Session,
    user_id: Optional[int],
    acao_tentada: str,
    motivo: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    ip_address: Optional[str] = None,
) -> AuditoriaLog:
    """
    Registra um acesso negado (violação de segurança)
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário
        acao_tentada: Ação que tentou fazer
        motivo: Motivo da negação
        resource_type: Tipo de recurso (opcional)
        resource_id: ID do recurso (opcional)
        ip_address: IP do cliente
        
    Returns:
        AuditoriaLog: Log criado
    """
    return registrar_evento_auditoria(
        db=db,
        event_type="SECURITY",
        action="ACCESS_DENIED",
        status="FAILURE",
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        error_message=motivo,
        context={"acao_tentada": acao_tentada},
        ip_address=ip_address,
    )


__all__ = [
    "registrar_evento_auditoria",
    "registrar_login_bem_sucedido",
    "registrar_falha_login",
    "registrar_operacao_crud",
    "registrar_acesso_negado",
]
