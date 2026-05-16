from pydantic_settings import BaseSettings

class Configuracion(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITMO: str = "HS256"
    MINUTOS_EXPIRACION_TOKEN: int = 30
    DIAS_EXPIRACION_REFRESH_TOKEN: int = 7

    class Config:
        env_file = ".env"

configuracion = Configuracion()