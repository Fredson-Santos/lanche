from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Objeto de configuração do Alembic que fornece
# acesso aos valores dentro do arquivo .ini em uso.
config = context.config

# Interpreta o arquivo de configuração para logging do Python.
# Esta linha configura os loggers basicamente.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adicione o objeto MetaData do seu modelo aqui
# para suporte 'autogenerate'
from app.models import usuario  # noqa
from app.db.database import Base
target_metadata = Base.metadata

# Outros valores da configuração, definidos pelas necessidades de env.py,
# podem ser adquiridos:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_sqlalchemy_url():
    """Obter URL do SQLAlchemy a partir do ambiente ou configuração"""
    url = os.getenv(
        "DATABASE_URL",
        config.get_main_option("sqlalchemy.url")
    )
    return url

def run_migrations_offline() -> None:
    """Executar migrações no modo 'offline'.

    Isso configura o contexto apenas com uma URL
    e não com uma Engine, embora uma Engine seja aceitável
    aqui também. Ao pular a criação da Engine
    não precisamos nem mesmo de um DBAPI disponível.

    As chamadas para context.execute() aqui emitem a string fornecida
    para a saída do script.

    """
    url = get_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executar migrações no modo 'online'.

    Neste cenário precisamos criar uma Engine
    e associar uma conexão com o contexto.

    """
    url = get_sqlalchemy_url()
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.StaticPool if "sqlite" in url else pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True if "sqlite" in url else False,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
