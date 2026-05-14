# Esquemas Pydantic para el presupuesto
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from typing import Optional
from pydantic import BaseModel


class PresupuestoBase(BaseModel):
    """Campos comunes compartidos entre esquemas de presupuesto."""
    importe_limite: float
    mes: int  # 1-12
    anio: int  # ej: 2025
    id_categoria: int


class PresupuestoCrear(PresupuestoBase):
    """
    Esquema para crear un nuevo presupuesto.
    El id_usuario se obtiene del token JWT, no del cuerpo de la petición.
    """
    pass


class PresupuestoActualizar(BaseModel):
    """
    Esquema para actualizar un presupuesto existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    importe_limite: Optional[float] = None
    mes: Optional[int] = None
    anio: Optional[int] = None
    id_categoria: Optional[int] = None


class PresupuestoRespuesta(PresupuestoBase):
    """
    Esquema de respuesta al cliente.
    Incluye el id y el id_usuario para identificar el presupuesto.
    """
    id: int
    id_usuario: int

    class Config:
        # Permite que Pydantic lea los datos desde atributos ORM
        from_attributes = True