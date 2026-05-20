# Esquemas Pydantic para el usuario
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    moneda: Optional[str] = "EUR"
    zona_horaria: Optional[str] = "Atlantic/Canary"


class UsuarioCrear(UsuarioBase):
    contrasena: str


class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    moneda: Optional[str] = None
    zona_horaria: Optional[str] = None
    contrasena: Optional[str] = None


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    moneda: str
    zona_horaria: str
    activo: bool
    es_admin: bool = False

    class Config:
        from_attributes = True


class TokenAcceso(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class DatosToken(BaseModel):
    email: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str