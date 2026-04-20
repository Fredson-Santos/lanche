"""
Tipos de coluna encriptados para SQLAlchemy
Define tipos customizados que encriptam/decriptam automaticamente dados
"""
from typing import Any, Optional
from sqlalchemy import TypeDecorator, String
from sqlalchemy.types import TypeEngine
from app.core.crypto import get_crypto_manager


class EncryptedString(TypeDecorator):
    """
    Tipo de coluna que encripta/decripta strings automaticamente
    
    Exemplo de uso:
        email = Column(EncryptedString, unique=False, index=False)
    
    Nota: Não use com índices ou colunas unique = True
    """
    
    impl = String
    cache_ok = True
    
    def process_bind_param(self, value: Any, dialect: Any) -> Optional[str]:
        """
        Encripta o valor antes de armazenar no banco
        """
        if value is None or value == "":
            return value
        
        crypto = get_crypto_manager()
        return crypto.encrypt(str(value))
    
    def process_result_value(self, value: Any, dialect: Any) -> Optional[str]:
        """
        Decripta o valor ao recuperar do banco
        """
        if value is None or value == "":
            return value
        
        crypto = get_crypto_manager()
        try:
            return crypto.decrypt(str(value))
        except ValueError:
            # Se falhar a decriptação, retorna o valor original (compatibilidade)
            return value


class SearchableEncryptedString(String):
    """
    Tipo de coluna para strings encriptadas com suporte a busca
    
    Implementa hash do valor para comparação sem descriptografar
    Ideal para campos como email onde precisamos fazer buscas
    
    Exemplo de uso:
        email = Column(SearchableEncryptedString, unique=True, index=True)
    """
    
    impl = String
    cache_ok = True
    
    def __init__(self, length: Optional[int] = None, **kwargs):
        super().__init__(length, **kwargs)
        self.encrypted = True
    
    def process_bind_param(self, value: Any, dialect: Any) -> Optional[str]:
        """
        Armazena o hash do valor para busca
        Em produção, combinaria com o valor encriptado
        """
        if value is None or value == "":
            return value
        
        import hashlib
        return hashlib.sha256(str(value).encode()).hexdigest()
    
    def process_result_value(self, value: Any, dialect: Any) -> Optional[str]:
        """
        Nota: SearchableEncrypted não retorna o valor original
        Use somente para verificações, não para leitura do dado
        """
        return value
