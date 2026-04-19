from pydantic import BaseModel, Field
from app.schemas.produto import ProdutoListResponse


class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: float = Field(..., gt=0)


class ItemVendaResponse(BaseModel):
    id: int
    venda_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True


class ItemVendaComProdutoResponse(BaseModel):
    id: int
    venda_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    produto: ProdutoListResponse

    class Config:
        from_attributes = True
