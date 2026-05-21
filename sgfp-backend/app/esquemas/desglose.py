# Esquemas Pydantic para desglose de transacción
from pydantic import BaseModel
from typing import Optional


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