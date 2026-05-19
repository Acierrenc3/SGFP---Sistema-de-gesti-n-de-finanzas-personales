# Esquemas Pydantic para transacciones recurrentes
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RecurrenteBase(BaseModel):
    """Campos comunes compartidos entre esquemas de recurrente."""
    tipo: str                    # 'ingreso' o 'gasto'
    importe: float
    descripcion: str
    frecuencia: str              # 'diario', 'semanal', 'mensual', 'anual'
    dia_repeticion: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    id_categoria: int
    id_cuenta: int


class RecurrenteCrear(RecurrenteBase):
    """Esquema para crear un nuevo recurrente."""
    pass


class RecurrenteActualizar(BaseModel):
    """Esquema para actualizar un recurrente existente."""
    tipo: Optional[str] = None
    importe: Optional[float] = None
    descripcion: Optional[str] = None
    frecuencia: Optional[str] = None
    dia_repeticion: Optional[int] = None
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = None
    id_categoria: Optional[int] = None
    id_cuenta: Optional[int] = None


class RecurrenteRespuesta(RecurrenteBase):
    """Esquema de respuesta al cliente."""
    id: int
    id_usuario: int
    proxima_ejecucion: datetime
    activo: bool

    class Config:
        from_attributes = True