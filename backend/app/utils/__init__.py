"""Utils - Helper functions, validators, exceptions"""
from app.utils.exceptions import (
    UsuarioNaoEncontrado,
    EmailJaExiste,
    UsernameJaExiste,
    CredenciaisInvalidas,
    TokenInvalido,
    SemPermissao,
    ProdutoNaoEncontrado,
    EstoqueInsuficiente,
    VendaNaoEncontrada,
    ErroInterno,
)
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_username,
    validate_preco,
    validate_quantidade,
)

__all__ = [
    "UsuarioNaoEncontrado",
    "EmailJaExiste",
    "UsernameJaExiste",
    "CredenciaisInvalidas",
    "TokenInvalido",
    "SemPermissao",
    "ProdutoNaoEncontrado",
    "EstoqueInsuficiente",
    "VendaNaoEncontrada",
    "ErroInterno",
    "validate_email",
    "validate_password",
    "validate_username",
    "validate_preco",
    "validate_quantidade",
]
