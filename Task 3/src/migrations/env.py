from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

# project imports (moved below after sys.path is updated)



# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- ensure project paths from alembic.ini are added to sys.path ---
# read raw value from config; support %(here)s and a few path_separator tokens
raw_prepend = config.get_main_option("prepend_sys_path") or ""
raw_sep = config.get_main_option("path_separator") or ""

# determine separator to split raw_prepend
if raw_sep == "os":
    sep = os.pathsep
elif raw_sep == "space":
    sep = " "
elif raw_sep == "newline":
    sep = "\n"
elif raw_sep:
    sep = raw_sep
else:
    # fallback: legacy splitting on commas/spaces/colons
    sep = None

# resolve %(here)s to directory of alembic.ini
here_dir = None
if config.config_file_name:
    here_dir = os.path.abspath(os.path.dirname(config.config_file_name))

# perform simple substitutions if present
if "%(here)s" in raw_prepend and here_dir:
    raw_prepend = raw_prepend.replace("%(here)s", here_dir)

if "%(path_separator)s" in raw_prepend:
    # expand to OS-specific separator
    raw_prepend = raw_prepend.replace("%(path_separator)s", os.pathsep)

paths = []
if sep:
    parts = [p.strip() for p in raw_prepend.split(sep) if p.strip()]
else:
    # legacy split: commas, spaces or colons
    import re

    parts = [p for p in re.split(r"[ ,:]+", raw_prepend) if p]

for p in parts:
    # if a relative path remains, make it relative to here_dir
    if not os.path.isabs(p) and here_dir:
        p = os.path.abspath(os.path.join(here_dir, p))
    paths.append(p)

# insert each path at front so first in list has highest precedence
for p in reversed(paths):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
# --- end prepend_sys_path handling ---

# now that sys.path is adjusted, import project modules
from src.config import settings
from src.database import BaseORM
from src.models.hotels import HotelsOrm

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseORM.metadata

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
