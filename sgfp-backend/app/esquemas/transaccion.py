# Esquemas Pydantic para la transacción
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TransaccionBase(BaseModel):
    """Campos comunes compartidos entre esquemas de transacción."""
    tipo: str  # 'ingreso' o 'gasto'
    importe: float
    fecha: datetime
    descripcion: Optional[str] = None
    id_categoria: int
    id_cuenta: int


class TransaccionCrear(TransaccionBase):
    """
    Esquema para crear una nueva transacción.
    El id_usuario se obtiene del token JWT, no del cuerpo de la petición.
    """
    pass


class TransaccionActualizar(BaseModel):
    """
    Esquema para actualizar una transacción existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    tipo: Optional[str] = None
    importe: Optional[float] = None
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_cuenta: Optional[int] = None


class TransaccionRespuesta(TransaccionBase):
    """
    Esquema de respuesta al cliente.
    Incluye el id y el id_usuario para identificar la transacción.
    """
    id: int
    id_usuario: int

    class Config:
        # Permite que Pydantic lea los datos desde atributos ORM
        from_attributes = True