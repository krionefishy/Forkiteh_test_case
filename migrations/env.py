from logging.config import fileConfig
import asyncio
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from app.repository.base import Base 
from alembic import context
from app.repository.models import WalletModel



config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata




def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"), 
        poolclass=pool.NullPool
        )
    
    async with connectable.connect() as connection:
        def run_migrations(conn):
            context.configure(
                connection=conn,
                target_metadata=target_metadata,
                compare_type=True
            )
            with context.begin_transaction():
                context.run_migrations()
        
        await connection.run_sync(run_migrations)
        
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())  # Изменено

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
