# Esquemas Pydantic para la cuenta
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from typing import Optional
from pydantic import BaseModel


class CuentaBase(BaseModel):
    """Campos comunes compartidos entre esquemas de cuenta."""
    nombre: str
    tipo: str  # 'efectivo', 'bancaria', 'tarjeta', 'ahorro'
    saldo_inicial: float = 0.0
    moneda: str = 'EUR'


class CuentaCrear(CuentaBase):
    """
    Esquema para crear una nueva cuenta.
    El id_usuario se obtiene del token JWT, no del cuerpo de la petición.
    """
    pass


class CuentaActualizar(BaseModel):
    """
    Esquema para actualizar una cuenta existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    saldo_inicial: Optional[float] = None
    moneda: Optional[str] = None


class CuentaRespuesta(CuentaBase):
    """
    Esquema de respuesta al cliente.
    Incluye el id y el id_usuario para identificar la cuenta.
    """
    id: int
    id_usuario: int

    class Config:
        from_attributes = True