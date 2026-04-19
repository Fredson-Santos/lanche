from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    quantidade = Column(Integer, default=0, nullable=False)
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    produto = relationship("Produto", backref="estoque")

    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_estoque_quantidade_nao_negativa"),
    )

    def __repr__(self):
        return f"<Estoque(produto_id={self.produto_id}, quantidade={self.quantidade})>"
