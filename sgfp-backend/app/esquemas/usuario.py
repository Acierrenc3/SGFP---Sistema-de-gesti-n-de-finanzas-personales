# Esquemas Pydantic para el usuario
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    """Campos comunes compartidos entre esquemas de usuario."""
    nombre: str
    email: EmailStr
    moneda: Optional[str] = "EUR"
    zona_horaria: Optional[str] = "Europe/Madrid"


class UsuarioCrear(UsuarioBase):
    """
    Esquema para el registro de un nuevo usuario.
    Incluye la contraseña en texto plano que será hasheada antes de guardar.
    """
    contrasena: str


class UsuarioActualizar(BaseModel):
    """
    Esquema para actualizar el perfil del usuario.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre: Optional[str] = None
    moneda: Optional[str] = None
    zona_horaria: Optional[str] = None
    contrasena: Optional[str] = None


class UsuarioRespuesta(UsuarioBase):
    """
    Esquema de respuesta al cliente.
    Nunca incluye la contraseña ni su hash.
    """
    id: int
    activo: bool

    class Config:
        # Permite que Pydantic lea los datos desde atributos ORM
        from_attributes = True


class TokenAcceso(BaseModel):
    """Esquema del token JWT devuelto tras el login."""
    access_token: str
    token_type: str


class DatosToken(BaseModel):
    """Datos extraídos del payload del token JWT."""
    email: Optional[str] = None