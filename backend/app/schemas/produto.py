from datetime import datetime
from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    descricao: str | None = None
    preco: float = Field(..., gt=0)


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=255)
    descricao: str | None = None
    preco: float | None = Field(None, gt=0)
    ativo: bool | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    id: int
    nome: str
    preco: float
    ativo: bool

    class Config:
        from_attributes = True
