"""
Modelo de Ordem de Reposição - Pedidos automáticos de reposição de estoque
RF-06: Reposição automática de estoque
"""

from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class StatusOrdemReposicao(str, Enum):
    """Status possíveis de uma ordem de reposição"""
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    RECEBIDA = "recebida"
    CANCELADA = "cancelada"


class OrdemReposicao(Base):
    __tablename__ = "ordens_reposicao"

    id = Column(Integer, primary_key=True, index=True)
    estoque_id = Column(Integer, ForeignKey("estoques.id", ondelete="CASCADE"), nullable=False, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True)
    quantidade_solicitada = Column(Integer, nullable=False)
    quantidade_recebida = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default=StatusOrdemReposicao.PENDENTE, nullable=False, index=True)
    motivo = Column(String(255), nullable=True)  # "automática" ou "manual"
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    data_confirmacao = Column(DateTime(timezone=True), nullable=True)
    data_recebimento = Column(DateTime(timezone=True), nullable=True)
    data_cancelamento = Column(DateTime(timezone=True), nullable=True)

    # Relacionamentos
    estoque = relationship("Estoque", backref="ordens_reposicao")
    produto = relationship("Produto", backref="ordens_reposicao")

    def __repr__(self):
        return f"<OrdemReposicao(id={self.id}, estoque_id={self.estoque_id}, status={self.status})>"
