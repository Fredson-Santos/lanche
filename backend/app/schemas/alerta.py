"""
Schemas de Alerta - Serialização e validação de dados de alertas
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TipoAlertaSchema(str, Enum):
    """Tipos de alertas disponíveis"""
    VALIDADE = "validade"
    TEMPERATURA = "temperatura"
    ESTOQUE_MINIMO = "estoque_minimo"


class AlertaCreate(BaseModel):
    """Schema para criação de alerta"""
    produto_id: int
    estoque_id: int | None = None
    tipo: TipoAlertaSchema
    titulo: str = Field(..., min_length=1, max_length=255)
    descricao: str | None = None


class AlertaUpdate(BaseModel):
    """Schema para atualização de alerta (marcar como lido)"""
    lido: bool | None = None
    ativo: bool | None = None


class AlertaResponse(BaseModel):
    """Schema de resposta para alerta"""
    id: int
    produto_id: int
    estoque_id: int | None
    tipo: TipoAlertaSchema
    titulo: str
    descricao: str | None
    lido: bool
    ativo: bool
    data_criacao: datetime
    data_leitura: datetime | None
    data_resolucao: datetime | None

    class Config:
        from_attributes = True


class AlertaListResponse(BaseModel):
    """Schema de resposta para lista de alertas"""
    id: int
    produto_id: int
    tipo: TipoAlertaSchema
    titulo: str
    lido: bool
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True
