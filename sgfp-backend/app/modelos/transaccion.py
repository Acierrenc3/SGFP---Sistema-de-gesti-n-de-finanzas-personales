# Modelo ORM de la transacción
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transaccion(Base):
    """
    Representa la tabla 'transacciones' en la base de datos.
    Registra cada movimiento financiero del usuario (ingreso o gasto),
    vinculado a una categoría y una cuenta.
    """

    __tablename__ = "transacciones"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Tipo de movimiento: 'ingreso' o 'gasto'
    tipo = Column(String(10), nullable=False)

    # Importe del movimiento en la moneda del usuario
    importe = Column(Float, nullable=False)

    # Fecha y hora del movimiento
    # Por defecto usa la fecha y hora actual en UTC
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Descripción opcional del movimiento (ej: Compra supermercado)
    descripcion = Column(String(255), nullable=True)

    # Clave foránea al usuario propietario
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Clave foránea a la categoría asociada
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # Clave foránea a la cuenta asociada
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)

    # Relaciones ORM
    usuario = relationship("Usuario", back_populates="transacciones")
    categoria = relationship("Categoria", back_populates="transacciones")
    cuenta = relationship("Cuenta", back_populates="transacciones")