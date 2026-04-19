import re
from pydantic import ValidationError


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    if not any(char.isupper() for char in password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"
    if not any(char.isdigit() for char in password):
        return False, "Senha deve conter pelo menos um dígito"
    return True, "Senha válida"


def validate_username(username: str) -> tuple[bool, str]:
    if len(username) < 3:
        return False, "Username deve ter no mínimo 3 caracteres"
    if len(username) > 100:
        return False, "Username não pode exceder 100 caracteres"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username pode conter apenas letras, números, _ e -"
    return True, "Username válido"


def validate_preco(preco: float) -> tuple[bool, str]:
    if preco <= 0:
        return False, "Preço deve ser maior que zero"
    if preco > 1000000:
        return False, "Preço excede o valor máximo permitido"
    return True, "Preço válido"


def validate_quantidade(quantidade: int) -> tuple[bool, str]:
    if quantidade < 0:
        return False, "Quantidade não pode ser negativa"
    if quantidade > 1000000:
        return False, "Quantidade excede o valor máximo permitido"
    return True, "Quantidade válida"
