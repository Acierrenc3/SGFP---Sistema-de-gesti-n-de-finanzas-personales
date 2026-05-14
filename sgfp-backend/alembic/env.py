# Configuración del entorno de migraciones Alembic
# Basado en: https://alembic.sqlalchemy.org/en/latest/tutorial.html

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Importa la configuración de la aplicación para obtener la URL de la BD
from app.core.configuracion import configuracion

# Importa Base y todos los modelos para que Alembic los detecte
from app.db.base import Base
from app.modelos import usuario, categoria, cuenta, transaccion, presupuesto

# Objeto de configuración de Alembic
config = context.config

# Interpreta el archivo de configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establece la URL de la base de datos desde la configuración de la app
config.set_main_option("sqlalchemy.url", configuracion.DATABASE_URL)

# Metadata de los modelos para las migraciones automáticas
target_metadata = Base.metadata


def ejecutar_migraciones_offline() -> None:
    """
    Ejecuta las migraciones en modo offline.
    No requiere conexión activa a la base de datos.
    Basado en: https://alembic.sqlalchemy.org/en/latest/offline.html
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


def ejecutar_migraciones_online() -> None:
    """
    Ejecuta las migraciones en modo online.
    Requiere conexión activa a la base de datos.
    Basado en: https://alembic.sqlalchemy.org/en/latest/online.html
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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


# Determina el modo de ejecución y lanza las migraciones
if context.is_offline_mode():
    ejecutar_migraciones_offline()
else:
    ejecutar_migraciones_online()