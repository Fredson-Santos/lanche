from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.db.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True, index=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("preco > 0", name="ck_produto_preco_positivo"),
    )

    def __repr__(self):
        return f"<Produto(id={self.id}, nome={self.nome}, preco={self.preco})>"
