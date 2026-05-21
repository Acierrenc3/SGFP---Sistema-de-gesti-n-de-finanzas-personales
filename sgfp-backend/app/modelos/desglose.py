# Modelo ORM de desglose de transacción
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class DesgloseTransaccion(Base):
    """Representa cada línea de desglose de una transacción."""

    __tablename__ = "desgloses_transaccion"

    id = Column(Integer, primary_key=True, index=True)
    concepto = Column(String(255), nullable=False)
    importe = Column(Float, nullable=False)
    id_transaccion = Column(Integer, ForeignKey("transacciones.id"), nullable=False)

    # Relación ORM
    transaccion = relationship("Transaccion", back_populates="desgloses")