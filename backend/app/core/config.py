"""
Configuração central da aplicação LANCHE MVP
Utiliza Pydantic Settings para validação e gestão de variáveis de ambiente
Carrega variáveis do arquivo .env via python-dotenv
"""

import logging
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pythonjsonlogger import jsonlogger

# Carrega variáveis de ambiente do arquivo .env
env_file = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_file, override=False)


class Settings(BaseSettings):
    """
    Configurações da aplicação com validação automática via Pydantic
    """

    # ========== DATABASE ==========
    DATABASE_URL: str = "sqlite:///./lanche.db"
    """URL de conexão com o banco de dados"""

    # ========== SECURITY ==========
    SECRET_KEY: str = "your-secret-key-change-in-production"
    """Chave secreta para assinatura de JWT"""

    ALGORITHM: str = "HS256"
    """Algoritmo para assinatura de tokens JWT"""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    """Tempo de expiração do token de acesso em minutos (padrão: 24 horas)"""

    # ========== LOGGING ==========
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    """Nível de logging da aplicação"""

    LOG_FORMAT: Literal["json", "standard"] = "json"
    """Formato de saída do logging (json ou standard)"""

    # ========== ENVIRONMENT ==========
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    """Ambiente de execução da aplicação"""

    DEBUG: bool = False
    """Modo debug ativado"""

    class Config:
        """Configuração do BaseSettings"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


def get_settings() -> Settings:
    """
    Factory function para obter instância de Settings com lazy loading
    """
    return Settings()


def setup_logging(settings: Settings) -> logging.Logger:
    """
    Configura logging estruturado (JSON) para a aplicação

    Args:
        settings: Instância de Settings com configurações

    Returns:
        Logger configurado pronto para uso

    Raises:
        ValueError: Se LOG_LEVEL inválido
    """
    logger = logging.getLogger("lanche")

    # Limpa handlers existentes
    logger.handlers.clear()

    # Define nível de logging
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    # Cria handler para stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Define formato baseado na configuração
    if settings.LOG_FORMAT == "json":
        formatter = jsonlogger.JsonFormatter(
            fmt="%(timestamp)s %(level)s %(name)s %(message)s",
            timestamp=True,
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Instâncias singleton
settings = get_settings()
logger = setup_logging(settings)

# Exportar para uso em toda a aplicação
__all__ = ["Settings", "settings", "logger", "get_settings", "setup_logging"]
