import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

sys.path.append(os.getcwd())

from src.config.settings import settings  
from src.db.session import Base           
from src.db.models import * 

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    """
    Получает URL из настроек и подменяет драйвер.
    Alembic работает синхронно, поэтому 'postgresql+asyncpg'
    нужно заменить на 'postgresql' (по умолчанию psycopg2).
    """
    url = str(settings.DATABASE_URL)
    if "postgresql+asyncpg" in url:
        return url.replace("postgresql+asyncpg", "postgresql")
    return url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    В этом режиме подключение к БД не создается, просто генерируется SQL скрипт.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    В этом режиме Alembic подключается к базе и применяет миграции.
    """
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()