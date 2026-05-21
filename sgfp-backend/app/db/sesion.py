# Configuración de la sesión de base de datos con SQLAlchemy
# Basado en: https://docs.sqlalchemy.org/en/20/orm/session_basics.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.configuracion import configuracion

# Crea el motor de conexión a PostgreSQL
# pool_pre_ping=True verifica la conexión antes de usarla
motor = create_engine(
    configuracion.DATABASE_URL,
    pool_pre_ping=True
)

# Fábrica de sesiones configurada
# autocommit=False → los cambios deben confirmarse explícitamente
# autoflush=False  → los cambios no se envían automáticamente a la BD
SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor
)


def obtener_sesion():
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    Garantiza el cierre de la sesión tras cada petición.
    Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
    """
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()

def obtener_sesion_sync():
    """Versión síncrona del generador de sesión para uso en WebSocket."""
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()