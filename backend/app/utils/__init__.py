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
from app.utils.audit import (
    registrar_evento_auditoria,
    registrar_login_bem_sucedido,
    registrar_falha_login,
    registrar_operacao_crud,
    registrar_acesso_negado,
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
    "registrar_evento_auditoria",
    "registrar_login_bem_sucedido",
    "registrar_falha_login",
    "registrar_operacao_crud",
    "registrar_acesso_negado",
]
