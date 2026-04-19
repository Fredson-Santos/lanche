from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.produto import ProdutoResponse


class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(default=0, ge=0)


class EstoqueUpdate(BaseModel):
    quantidade: int = Field(ge=0)


class EstoqueResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    data_atualizacao: datetime

    class Config:
        from_attributes = True


class EstoqueComProdutoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    produto: ProdutoResponse
    data_atualizacao: datetime

    class Config:
        from_attributes = True
