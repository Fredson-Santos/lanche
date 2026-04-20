"""
Modelo de Alertas - Validade, Temperatura e Estoque Mínimo
RF-01, RF-02, RF-03: Alertas de validade, temperatura e reposição
"""

from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class TipoAlerta(str, Enum):
    """Tipos de alertas disponíveis"""
    VALIDADE = "validade"
    TEMPERATURA = "temperatura"
    ESTOQUE_MINIMO = "estoque_minimo"


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True)
    estoque_id = Column(Integer, ForeignKey("estoques.id", ondelete="CASCADE"), nullable=True, index=True)
    tipo = Column(String(50), nullable=False, index=True)  # validade, temperatura, estoque_minimo
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    lido = Column(Boolean, default=False, index=True)
    ativo = Column(Boolean, default=True, index=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    data_leitura = Column(DateTime(timezone=True), nullable=True)
    data_resolucao = Column(DateTime(timezone=True), nullable=True)

    # Relacionamentos
    produto = relationship("Produto", backref="alertas")
    estoque = relationship("Estoque", backref="alertas")

    def __repr__(self):
        return f"<Alerta(id={self.id}, tipo={self.tipo}, produto_id={self.produto_id}, lido={self.lido})>"
