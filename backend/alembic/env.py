
from logging.config import fileConfig

from alembic import context

from app.infrastructure.database.base import Base
from app.infrastructure.database.session import DATABASE_URL, engine

# Register the Inventory model with SQLAlchemy metadata.
from app.features.inventory import models as inventory_models  # noqa: F401
from app.features.auth import models as auth_models  # noqa: F401

from app.features.products import models as product_models


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
