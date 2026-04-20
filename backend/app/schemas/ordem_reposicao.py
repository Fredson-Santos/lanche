"""
Schemas de Ordem de Reposição - Serialização e validação de dados
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class StatusOrdemReposicaoSchema(str, Enum):
    """Status possíveis de uma ordem de reposição"""
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    RECEBIDA = "recebida"
    CANCELADA = "cancelada"


class OrdemReposicaoCreate(BaseModel):
    """Schema para criação de ordem de reposição"""
    estoque_id: int
    produto_id: int
    quantidade_solicitada: int = Field(..., gt=0)
    motivo: str | None = None  # "automática" ou "manual"
    observacoes: str | None = None


class OrdemReposicaoUpdate(BaseModel):
    """Schema para atualização de ordem de reposição"""
    status: StatusOrdemReposicaoSchema | None = None
    quantidade_recebida: int | None = Field(None, ge=0)
    observacoes: str | None = None


class OrdemReposicaoResponse(BaseModel):
    """Schema de resposta para ordem de reposição"""
    id: int
    estoque_id: int
    produto_id: int
    quantidade_solicitada: int
    quantidade_recebida: int
    status: StatusOrdemReposicaoSchema
    motivo: str | None
    observacoes: str | None
    data_criacao: datetime
    data_confirmacao: datetime | None
    data_recebimento: datetime | None
    data_cancelamento: datetime | None

    class Config:
        from_attributes = True


class OrdemReposicaoListResponse(BaseModel):
    """Schema de resposta para lista de ordens"""
    id: int
    estoque_id: int
    produto_id: int
    quantidade_solicitada: int
    quantidade_recebida: int
    status: StatusOrdemReposicaoSchema
    motivo: str | None
    data_criacao: datetime

    class Config:
        from_attributes = True
