from app.esquemas.desglose import DesgloseRespuesta
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


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