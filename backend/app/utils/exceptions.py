from fastapi import HTTPException, status


class UsuarioNaoEncontrado(HTTPException):
    def __init__(self, detail: str = "Usuario não encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class EmailJaExiste(HTTPException):
    def __init__(self, detail: str = "Email já registrado"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class UsernameJaExiste(HTTPException):
    def __init__(self, detail: str = "Username já registrado"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class CredenciaisInvalidas(HTTPException):
    def __init__(self, detail: str = "Email ou senha incorretos"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenInvalido(HTTPException):
    def __init__(self, detail: str = "Token inválido ou expirado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class SemPermissao(HTTPException):
    def __init__(self, detail: str = "Acesso negado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class ProdutoNaoEncontrado(HTTPException):
    def __init__(self, detail: str = "Produto não encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class EstoqueInsuficiente(HTTPException):
    def __init__(self, detail: str = "Estoque insuficiente"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class VendaNaoEncontrada(HTTPException):
    def __init__(self, detail: str = "Venda não encontrada"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ErroInterno(HTTPException):
    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
