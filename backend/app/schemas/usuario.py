from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    senha: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=100)
    ativo: bool | None = None


class UsuarioResponse(BaseModel):
    id: int
    email: str
    username: str
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
