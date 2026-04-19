from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False, index=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", backref="itens_venda")

    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_item_venda_quantidade_positiva"),
        CheckConstraint("preco_unitario > 0", name="ck_item_venda_preco_positivo"),
    )

    def __repr__(self):
        return f"<ItemVenda(venda_id={self.venda_id}, produto_id={self.produto_id}, quantidade={self.quantidade})>"
