from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.item_venda import ItemVendaCreate, ItemVendaComProdutoResponse


class VendaCreate(BaseModel):
    usuario_id: int
    itens: list[ItemVendaCreate] = Field(..., min_items=1)


class VendaResponse(BaseModel):
    id: int
    usuario_id: int
    total: float
    data_venda: datetime
    itens: list[ItemVendaComProdutoResponse]
    data_criacao: datetime

    class Config:
        from_attributes = True


class VendaListResponse(BaseModel):
    id: int
    usuario_id: int
    total: float
    data_venda: datetime
    quantidade_itens: int | None = None

    class Config:
        from_attributes = True
