import pkgutil
import importlib
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# NEW
# Automatically discover and import all models in the app.domain package
def load_models(package_name):
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package_name}.{module_name}")

# NEW
# Call the function to load all models
load_models("app.domain")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None # COMMENTED
from app.domain.base_entity import BaseEntity  # NEW
target_metadata = BaseEntity.metadata # UPDATED

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


#
# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine
# from alembic import context
#
# # Import your models and settings
# from app.domain import Base
# from app.core.config import settings
#
# target_metadata = Base.metadata
#
# async def run_migrations_online():
#     """Run migrations in 'online' mode."""
#     # Create async engine
#     connectable = create_async_engine("postgresql+asyncpg://chatdocuser:PassWord123@localhost:5432/chatdocdb")
#     # connectable = create_async_engine(settings.DATABASE_URL)
#
#     # Use the async engine to connect and run migrations
#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)
#
# def do_run_migrations(connection):
#     """Run migration logic."""
#     context.configure(connection=connection, target_metadata=target_metadata)
#     with context.begin_transaction():
#         context.run_migrations()
#
# def run_migrations_offline():
#     """Run migrations in 'offline' mode."""
#     url = settings.DATABASE_URL
#     context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
#     with context.begin_transaction():
#         context.run_migrations()
#
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())

