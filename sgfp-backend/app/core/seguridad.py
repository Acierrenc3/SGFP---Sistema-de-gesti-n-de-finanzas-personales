# Gestión de seguridad: cifrado de contraseñas y tokens JWT
# Basado en:
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://pypi.org/project/bcrypt/

from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.configuracion import configuracion


def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    """Compara una contraseña en texto plano con su hash almacenado."""
    return bcrypt.checkpw(
        contraseña_plana.encode("utf-8"),
        contraseña_hash.encode("utf-8")
    )


def obtener_hash_contraseña(contraseña: str) -> str:
    """Genera el hash bcrypt de una contraseña."""
    sal = bcrypt.gensalt()
    return bcrypt.hashpw(contraseña.encode("utf-8"), sal).decode("utf-8")


def crear_token_acceso(datos: dict, expiracion: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado con los datos del usuario.
    Si no se indica expiración, usa el valor definido en configuración.
    """
    datos_token = datos.copy()

    if expiracion:
        expira = datetime.utcnow() + expiracion
    else:
        expira = datetime.utcnow() + timedelta(
            minutes=configuracion.MINUTOS_EXPIRACION_TOKEN
        )

    datos_token.update({"exp": expira})

    token = jwt.encode(
        datos_token,
        configuracion.SECRET_KEY,
        algorithm=configuracion.ALGORITMO
    )

    return token


def decodificar_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT.
    Devuelve el payload si es válido, None si no lo es.
    """
    try:
        payload = jwt.decode(
            token,
            configuracion.SECRET_KEY,
            algorithms=[configuracion.ALGORITMO]
        )
        return payload
    except JWTError:
        return None