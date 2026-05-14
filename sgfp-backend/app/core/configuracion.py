# Configuración central de la aplicación
# Basado en: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

from pydantic_settings import BaseSettings

class Configuracion(BaseSettings):
    # URL de conexión a la base de datos PostgreSQL
    DATABASE_URL: str

    # Clave secreta para firmar los tokens JWT
    SECRET_KEY: str

    # Algoritmo de cifrado para JWT (por defecto HS256)
    ALGORITMO: str = "HS256"

    # Tiempo de expiración del token en minutos
    MINUTOS_EXPIRACION_TOKEN: int = 30

    class Config:
        # Pydantic lee automáticamente las variables del archivo .env
        env_file = ".env"


# Instancia global de configuración accesible desde cualquier módulo
configuracion = Configuracion()