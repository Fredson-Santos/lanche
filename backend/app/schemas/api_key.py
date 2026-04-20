"""
Schemas de validação para API Keys - Pydantic
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    """Schema para criar nova API key"""
    descricao: str = Field(..., min_length=3, max_length=255, description="Descrição da chave")
    limite_requisicoes: int = Field(default=100, ge=1, le=10000, description="Limite de requisições")
    janela_tempo: int = Field(default=60, ge=1, le=1440, description="Janela de tempo em minutos")
    expires_em: Optional[datetime] = Field(None, description="Data de expiração (opcional)")


class APIKeyUpdate(BaseModel):
    """Schema para atualizar API key"""
    ativo: Optional[bool] = Field(None, description="Ativar/desativar chave")
    descricao: Optional[str] = Field(None, min_length=3, max_length=255, description="Descrição")
    limite_requisicoes: Optional[int] = Field(None, ge=1, le=10000, description="Limite")
    expires_em: Optional[datetime] = Field(None, description="Data de expiração")


class APIKeyResponse(BaseModel):
    """Schema de resposta para API key"""
    id: int
    chave: str
    ativo: bool
    limite_requisicoes: int
    janela_tempo: int
    criado_em: datetime
    expires_em: Optional[datetime]
    ultima_uso: Optional[datetime]
    descricao: Optional[str]
    
    class Config:
        from_attributes = True


class APIKeyListResponse(BaseModel):
    """Schema de resposta para listar API keys (sem expor a chave completa)"""
    id: int
    chave: str  # Apenas primeiros 8 caracteres na prática
    ativo: bool
    descricao: Optional[str]
    criado_em: datetime
    expires_em: Optional[datetime]
    ultima_uso: Optional[datetime]
    
    class Config:
        from_attributes = True


class APIKeyCreateResponse(BaseModel):
    """Schema de resposta ao criar API key (mostra a chave uma única vez)"""
    id: int
    chave: str  # Completa, mostrada uma única vez
    ativo: bool
    descricao: Optional[str]
    criado_em: datetime
    message: str = "⚠️ Guarde esta chave com segurança. Ela não será mostrada novamente!"
    
    class Config:
        from_attributes = True


class APIKeyValidationResponse(BaseModel):
    """Schema de resposta da validação de API key"""
    valida: bool
    chave_id: Optional[int] = None
    mensagem: str
