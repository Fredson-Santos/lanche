from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    total = Column(Float, nullable=False)
    data_venda = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", backref="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("total > 0", name="ck_venda_total_positivo"),
    )

    def __repr__(self):
        return f"<Venda(id={self.id}, usuario_id={self.usuario_id}, total={self.total})>"
