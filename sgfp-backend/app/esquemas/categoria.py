# Esquemas Pydantic para la categoría
# Basado en: https://docs.pydantic.dev/latest/concepts/models/

from typing import Optional
from pydantic import BaseModel


class CategoriaBase(BaseModel):
    """Campos comunes compartidos entre esquemas de categoría."""
    nombre: str
    icono: Optional[str] = None
    color: Optional[str] = None
    tipo: str  # 'ingreso' o 'gasto'


class CategoriaCrear(CategoriaBase):
    """
    Esquema para crear una nueva categoría.
    id_usuario es opcional para permitir categorías predefinidas del sistema.
    """
    id_usuario: Optional[int] = None


class CategoriaActualizar(BaseModel):
    """
    Esquema para actualizar una categoría existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None
    tipo: Optional[str] = None


class CategoriaRespuesta(CategoriaBase):
    """
    Esquema de respuesta al cliente.
    Incluye el id y el id_usuario para identificar la categoría.
    """
    id: int
    id_usuario: Optional[int] = None

    class Config:
        # Permite que Pydantic lea los datos desde atributos ORM
        from_attributes = True