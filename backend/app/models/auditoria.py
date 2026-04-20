"""Modelo de Auditoria - Modelo ORM do SQLAlchemy para tabela de logs de auditoria"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.db.database import Base


class AuditoriaLog(Base):
    """
    Modelo para armazenar logs de auditoria
    Registra todas as operações críticas do sistema
    """
    __tablename__ = "auditoria_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação do evento
    event_type = Column(String(50), nullable=False, index=True)
    """Tipo de evento: AUTH, CRUD, SECURITY, SYSTEM"""
    
    action = Column(String(100), nullable=False, index=True)
    """Ação realizada: LOGIN, CREATE, UPDATE, DELETE, FAILED_LOGIN"""
    
    status = Column(String(20), nullable=False, default="SUCCESS", index=True)
    """Status: SUCCESS, FAILURE, PARTIAL"""
    
    # Contexto do usuário
    user_id = Column(Integer, nullable=True, index=True)
    """ID do usuário que realizou a ação"""
    
    # Informações do recurso
    resource_type = Column(String(50), nullable=True, index=True)
    """Tipo de recurso: Usuario, Produto, Venda, etc"""
    
    resource_id = Column(Integer, nullable=True, index=True)
    """ID do recurso afetado"""
    
    # Dados adicionais
    error_message = Column(Text, nullable=True)
    """Mensagem de erro se o status for FAILURE"""
    
    context = Column(JSON, nullable=True)
    """Contexto estruturado em JSON com detalhes da operação"""
    
    # Informações HTTP (quando aplicável)
    http_method = Column(String(10), nullable=True)
    """Método HTTP: GET, POST, PUT, DELETE"""
    
    http_path = Column(String(255), nullable=True)
    """Caminho da requisição HTTP"""
    
    http_status = Column(Integer, nullable=True)
    """Código de status HTTP da resposta"""
    
    ip_address = Column(String(45), nullable=True)
    """Endereço IP do cliente"""
    
    # Timestamps
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    """Data e hora do evento"""
    
    # Retenção de dados
    retencao_ativa = Column(Boolean, default=True)
    """Indica se o log está sob retenção (não deve ser deletado)"""

    def __repr__(self):
        return (
            f"<AuditoriaLog(id={self.id}, event_type={self.event_type}, "
            f"action={self.action}, status={self.status}, user_id={self.user_id})>"
        )
