"""
Módulo de Logging Estruturado para LANCHE MVP
Implementa logging centralizado com JSON formatter e suporte a auditoria
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from pythonjsonlogger import jsonlogger


class AuditJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formatter customizado para logs de auditoria em JSON
    Adiciona campos de contexto e timestamp estruturado
    """

    def add_fields(self, log_record: Dict, record: logging.LogRecord, message_dict: Dict):
        """
        Adiciona campos customizados aos logs
        
        Args:
            log_record: Dicionário do log
            record: LogRecord original
            message_dict: Dicionário de mensagens
        """
        super(AuditJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Adiciona campo de timestamp estruturado
        if "timestamp" not in log_record:
            log_record["timestamp"] = datetime.utcnow().isoformat()
        
        # Adiciona nível de severidade
        log_record["severity"] = record.levelname.lower()
        
        # Adiciona módulo e linha de código
        log_record["module"] = record.module
        log_record["line"] = record.lineno
        log_record["function"] = record.funcName


class StructuredLogger:
    """
    Logger estruturado para auditoria de eventos na aplicação
    Centraliza logging com formato JSON e atributos contextuais
    """

    def __init__(self, name: str, level: str = "INFO"):
        """
        Inicializa logger estruturado
        
        Args:
            name: Nome do logger
            level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.handlers.clear()
        
        # Configura nível
        self.logger.setLevel(getattr(logging, level, logging.INFO))
        
        # Handler para stdout com JSON
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level, logging.INFO))
        
        # Aplica formatter customizado
        formatter = AuditJsonFormatter(
            fmt="%(timestamp)s %(severity)s %(name)s %(message)s",
            timestamp=True,
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_event(
        self,
        event_type: str,
        action: str,
        status: str,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ):
        """
        Log de evento estruturado com contexto de auditoria
        
        Args:
            event_type: Tipo de evento (AUTH, CRUD, SECURITY, etc)
            action: Ação realizada (LOGIN, CREATE, UPDATE, DELETE, etc)
            status: Status do evento (SUCCESS, FAILURE, PARTIAL)
            user_id: ID do usuário (opcional)
            resource_type: Tipo de recurso afetado (opcional)
            resource_id: ID do recurso (opcional)
            details: Dicionário com detalhes adicionais (opcional)
            error_message: Mensagem de erro se aplicável (opcional)
        """
        log_data = {
            "event_type": event_type,
            "action": action,
            "status": status,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "error": error_message,
        }
        
        # Adiciona detalhes estruturados
        if details:
            log_data.update({"context": details})
        
        # Determina nível de log baseado no status
        log_level = logging.ERROR if status == "FAILURE" else logging.INFO
        
        # Converte para string JSON para logging
        message = json.dumps(log_data, ensure_ascii=False, default=str)
        self.logger.log(log_level, message)

    def info(self, message: str, **kwargs):
        """Log nível INFO com contexto adicional"""
        data = {"message": message}
        data.update(kwargs)
        self.logger.info(json.dumps(data, ensure_ascii=False, default=str))

    def warning(self, message: str, **kwargs):
        """Log nível WARNING com contexto adicional"""
        data = {"message": message}
        data.update(kwargs)
        self.logger.warning(json.dumps(data, ensure_ascii=False, default=str))

    def error(self, message: str, **kwargs):
        """Log nível ERROR com contexto adicional"""
        data = {"message": message}
        data.update(kwargs)
        self.logger.error(json.dumps(data, ensure_ascii=False, default=str))

    def debug(self, message: str, **kwargs):
        """Log nível DEBUG com contexto adicional"""
        data = {"message": message}
        data.update(kwargs)
        self.logger.debug(json.dumps(data, ensure_ascii=False, default=str))


# Singleton global do logger de auditoria
audit_logger = StructuredLogger("lanche.audit", level="INFO")


__all__ = ["StructuredLogger", "AuditJsonFormatter", "audit_logger"]
