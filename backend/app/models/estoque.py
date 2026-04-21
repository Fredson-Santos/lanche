from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from app.db.database import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    quantidade = Column(Integer, default=0, nullable=False)
    # Campos para reposição automática (RF-06)
    estoque_minimo = Column(Integer, default=0, nullable=False)
    estoque_maximo = Column(Integer, default=100, nullable=False)
    ponto_reposicao = Column(Integer, default=10, nullable=False)
    # Campos para alertas (RF-02, RF-03)
    temperatura_atual = Column(Float, nullable=True)
    data_ultima_verificacao = Column(DateTime(timezone=True), nullable=True)
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    produto = relationship("Produto", backref=backref("estoque", cascade="all, delete-orphan", uselist=False))

    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_estoque_quantidade_nao_negativa"),
    )

    def __repr__(self):
        return f"<Estoque(produto_id={self.produto_id}, quantidade={self.quantidade})>"
