# Gestión de seguridad: cifrado de contraseñas y tokens JWT
# Basado en:
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.configuracion import configuracion

# Contexto de cifrado usando bcrypt
# bcrypt es el esquema recomendado para contraseñas
contexto_cifrado = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    """Compara una contraseña en texto plano con su hash almacenado."""
    return contexto_cifrado.verify(contraseña_plana, contraseña_hash)


def obtener_hash_contraseña(contraseña: str) -> str:
    """Genera el hash bcrypt de una contraseña."""
    return contexto_cifrado.hash(contraseña)


def crear_token_acceso(datos: dict, expiracion: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado con los datos del usuario.
    Si no se indica expiración, usa el valor definido en configuración.
    """
    datos_token = datos.copy()

    # Calcula el tiempo de expiración
    if expiracion:
        expira = datetime.utcnow() + expiracion
    else:
        expira = datetime.utcnow() + timedelta(
            minutes=configuracion.MINUTOS_EXPIRACION_TOKEN
        )

    # Añade la claim de expiración al payload del token
    datos_token.update({"exp": expira})

    # Codifica y firma el token JWT
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