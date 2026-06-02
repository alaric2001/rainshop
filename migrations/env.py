import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# Baca app/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'app', '.env'))

# Import semua model agar autogenerate bisa mendeteksi perubahan skema
from app.database import Base
import app.models.itembarang     # noqa
import app.models.item_images    # noqa
import app.models.sales          # noqa
import app.models.vw_itembarang  # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Build URL dari .env — override alembic.ini
DB_HOST     = os.getenv('DB_HOST', 'localhost')
DB_PORT     = os.getenv('DB_PORT', '3306')
DB_USER     = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME     = os.getenv('DB_NAME', 'rainshop')

if DB_PASSWORD:
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    db_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

config.set_main_option('sqlalchemy.url', db_url)

target_metadata = Base.metadata

# View dan stored procedure tidak di-track Alembic (hanya tabel fisik)
_EXCLUDE = {'vw_itembarang', 'vw_sales_line'}

def include_object(object, name, type_, reflected, compare_to):
    if type_ == 'table' and name in _EXCLUDE:
        return False
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_object=include_object,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
