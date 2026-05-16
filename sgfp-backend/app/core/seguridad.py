from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.configuracion import configuracion


def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return bcrypt.checkpw(
        contraseña_plana.encode("utf-8"),
        contraseña_hash.encode("utf-8")
    )


def obtener_hash_contraseña(contraseña: str) -> str:
    sal = bcrypt.gensalt()
    return bcrypt.hashpw(contraseña.encode("utf-8"), sal).decode("utf-8")


def crear_token_acceso(datos: dict, expiracion: Optional[timedelta] = None) -> str:
    """Genera un token JWT de acceso de corta duración."""
    datos_token = datos.copy()
    expira = datetime.utcnow() + (
        expiracion or timedelta(minutes=configuracion.MINUTOS_EXPIRACION_TOKEN)
    )
    datos_token.update({"exp": expira, "tipo": "acceso"})
    return jwt.encode(datos_token, configuracion.SECRET_KEY, algorithm=configuracion.ALGORITMO)


def crear_refresh_token(datos: dict) -> str:
    """Genera un token JWT de refresco de larga duración."""
    datos_token = datos.copy()
    expira = datetime.utcnow() + timedelta(days=configuracion.DIAS_EXPIRACION_REFRESH_TOKEN)
    datos_token.update({"exp": expira, "tipo": "refresh"})
    return jwt.encode(datos_token, configuracion.SECRET_KEY, algorithm=configuracion.ALGORITMO)


def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica y valida un token JWT."""
    try:
        payload = jwt.decode(
            token,
            configuracion.SECRET_KEY,
            algorithms=[configuracion.ALGORITMO]
        )
        return payload
    except JWTError:
        return None