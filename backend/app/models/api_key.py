"""
Modelo de Chave de API para terceiros - RF-11
Suporta autenticação de aplicações externas (delivery, parceiros)
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint, Index
from sqlalchemy.sql import func

from app.db.database import Base


class APIKey(Base):
    """
    Chave de API para acesso de terceiros
    
    Campos:
    - chave: UUID v4 da chave (gerada automaticamente)
    - ativo: Se a chave está ativa ou revogada
    - limite_requisicoes: Limite de requisições na janela de tempo
    - janela_tempo: Duração da janela em minutos (padrão: 60)
    - criado_em: Timestamp de criação
    - expires_em: Data de expiração (NULL = nunca expira)
    - ultima_uso: Última vez que a chave foi usada
    - requisicoes_usadas: Contador de requisições na janela atual
    - descricao: Descrição da chave (ex: "Delivery A", "Parceiro B")
    """
    
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(64), unique=True, nullable=False, index=True)
    ativo = Column(Boolean, default=True, nullable=False)
    limite_requisicoes = Column(Integer, default=100, nullable=False)
    janela_tempo = Column(Integer, default=60, nullable=False)  # em minutos
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_em = Column(DateTime(timezone=True), nullable=True)
    ultima_uso = Column(DateTime(timezone=True), nullable=True)
    requisicoes_usadas = Column(Integer, default=0, nullable=False)
    descricao = Column(String(255), nullable=True)
    
    __table_args__ = (
        CheckConstraint('limite_requisicoes > 0', name='check_limite_requisicoes_positivo'),
        CheckConstraint('janela_tempo > 0', name='check_janela_tempo_positiva'),
        Index('ix_api_keys_chave_ativo', 'chave', 'ativo'),
        Index('ix_api_keys_criado_em', 'criado_em'),
        Index('ix_api_keys_expires_em', 'expires_em'),
    )
    
    def __repr__(self):
        return f"<APIKey chave={self.chave[:8]}... ativo={self.ativo}>"
    
    def esta_expirada(self) -> bool:
        """Verifica se a chave expirou"""
        if self.expires_em is None:
            return False
        return datetime.utcnow() > self.expires_em
    
    def esta_ativa(self) -> bool:
        """Verifica se a chave está ativa e não expirada"""
        return self.ativo and not self.esta_expirada()
