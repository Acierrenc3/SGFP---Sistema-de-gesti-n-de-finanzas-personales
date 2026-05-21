# Esquemas Pydantic para transacciones
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class DesgloseBase(BaseModel):
    concepto: str
    importe: float


class DesgloseCrear(DesgloseBase):
    pass


class DesgloseRespuesta(DesgloseBase):
    id: int
    id_transaccion: int

    class Config:
        from_attributes = True


class TransaccionBase(BaseModel):
    tipo: str
    importe: float
    fecha: datetime
    descripcion: Optional[str] = None
    id_categoria: int
    id_cuenta: int


class TransaccionCrear(TransaccionBase):
    desgloses: Optional[List[DesgloseCrear]] = []


class TransaccionActualizar(BaseModel):
    tipo: Optional[str] = None
    importe: Optional[float] = None
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_cuenta: Optional[int] = None
    desgloses: Optional[List[DesgloseCrear]] = None


class TransaccionRespuesta(TransaccionBase):
    id: int
    id_usuario: int
    desgloses: List[DesgloseRespuesta] = []

    class Config:
        from_attributes = True