from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.produto import ProdutoResponse


class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(default=0, ge=0)
    # Campos de reposição (RF-06)
    estoque_minimo: int = Field(default=0, ge=0)
    estoque_maximo: int = Field(default=100, ge=0)
    ponto_reposicao: int = Field(default=10, ge=0)
    # Campos para alertas (RF-02)
    temperatura_atual: float | None = None


class EstoqueUpdate(BaseModel):
    quantidade: int = Field(ge=0)
    # Campos de reposição (RF-06)
    estoque_minimo: int | None = Field(None, ge=0)
    estoque_maximo: int | None = Field(None, ge=0)
    ponto_reposicao: int | None = Field(None, ge=0)
    # Campo de temperatura para atualização
    temperatura_atual: float | None = None


class EstoqueResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    estoque_minimo: int
    estoque_maximo: int
    ponto_reposicao: int
    temperatura_atual: float | None
    data_atualizacao: datetime

    class Config:
        from_attributes = True


class EstoqueComProdutoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    estoque_minimo: int
    estoque_maximo: int
    ponto_reposicao: int
    temperatura_atual: float | None
    produto: ProdutoResponse
    data_atualizacao: datetime

    class Config:
        from_attributes = True
