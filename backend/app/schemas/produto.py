from datetime import datetime
from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    descricao: str | None = None
    preco: float = Field(..., gt=0)
    categoria: str = Field(default="outros", max_length=100)
    # Novos campos para alertas (RF-01, RF-02)
    data_validade: datetime | None = None
    lote: str | None = Field(None, max_length=100)
    temperatura_ideal_min: float | None = None
    temperatura_ideal_max: float | None = None


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=255)
    descricao: str | None = None
    preco: float | None = Field(None, gt=0)
    categoria: str | None = Field(None, max_length=100)
    ativo: bool | None = None
    # Campos de alerta para atualização
    data_validade: datetime | None = None
    lote: str | None = Field(None, max_length=100)
    temperatura_ideal_min: float | None = None
    temperatura_ideal_max: float | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    categoria: str
    ativo: bool
    data_validade: datetime | None
    lote: str | None
    temperatura_ideal_min: float | None
    temperatura_ideal_max: float | None
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    id: int
    nome: str
    preco: float
    categoria: str
    ativo: bool

    class Config:
        from_attributes = True
