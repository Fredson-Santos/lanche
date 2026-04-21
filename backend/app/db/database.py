"""Configuração de banco de dados e gerenciamento de sessão"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obter URL do banco de dados a partir do ambiente ou usar SQLite padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./lanche.db"
)

# Criar engine com configurações apropriadas
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,  # Recomendado para Postgres para evitar erros de conexão perdida
)

# Criar factory de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base declarativa para modelos
Base = declarative_base()


def get_db():
    """Dependência para obter sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar banco de dados - criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)
