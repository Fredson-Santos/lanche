"""Schemas de Auditoria - Validação de dados de logs de auditoria com Pydantic"""
from datetime import datetime
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field


class AuditoriaLogCreate(BaseModel):
    """Schema para criação de log de auditoria"""
    event_type: Literal["AUTH", "CRUD", "SECURITY", "SYSTEM"]
    action: str = Field(..., min_length=1, max_length=100)
    status: Literal["SUCCESS", "FAILURE", "PARTIAL"] = "SUCCESS"
    user_id: Optional[int] = None
    resource_type: Optional[str] = Field(None, max_length=50)
    resource_id: Optional[int] = None
    error_message: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    http_method: Optional[str] = Field(None, max_length=10)
    http_path: Optional[str] = Field(None, max_length=255)
    http_status: Optional[int] = None
    ip_address: Optional[str] = Field(None, max_length=45)


class AuditoriaLogResponse(BaseModel):
    """Schema para resposta de log de auditoria"""
    id: int
    event_type: str
    action: str
    status: str
    user_id: Optional[int]
    resource_type: Optional[str]
    resource_id: Optional[int]
    error_message: Optional[str]
    context: Optional[Dict[str, Any]]
    http_method: Optional[str]
    http_path: Optional[str]
    http_status: Optional[int]
    ip_address: Optional[str]
    data_criacao: datetime
    retencao_ativa: bool

    class Config:
        from_attributes = True


class AuditoriaLogFilter(BaseModel):
    """Schema para filtros de consulta de logs"""
    event_type: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)


class AuditoriaStatistics(BaseModel):
    """Schema para estatísticas de auditoria"""
    total_eventos: int
    eventos_por_status: Dict[str, int]
    eventos_por_tipo: Dict[str, int]
    eventos_por_acao: Dict[str, int]
    usuario_mais_ativo: Optional[int] = None
    periodo_analise: Dict[str, str]


__all__ = [
    "AuditoriaLogCreate",
    "AuditoriaLogResponse",
    "AuditoriaLogFilter",
    "AuditoriaStatistics",
]
