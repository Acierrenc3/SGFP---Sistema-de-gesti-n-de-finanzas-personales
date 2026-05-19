# Modelo ORM de transacción recurrente
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Recurrente(Base):
    """
    Representa la tabla 'recurrentes' en la base de datos.
    Define transacciones que se repiten automáticamente.
    """

    __tablename__ = "recurrentes"

    id = Column(Integer, primary_key=True, index=True)

    # Tipo de movimiento: 'ingreso' o 'gasto'
    tipo = Column(String(10), nullable=False)

    # Importe del movimiento
    importe = Column(Float, nullable=False)

    # Descripción del movimiento recurrente
    descripcion = Column(String(255), nullable=False)

    # Frecuencia: 'diario', 'semanal', 'mensual', 'anual'
    frecuencia = Column(String(10), nullable=False)

    # Día del mes o semana en que se repite (1-31 para mensual, 1-7 para semanal)
    dia_repeticion = Column(Integer, nullable=True)

    # Fecha de inicio del recurrente
    fecha_inicio = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Fecha de fin del recurrente (None = sin fin)
    fecha_fin = Column(DateTime, nullable=True)

    # Fecha de la próxima ejecución
    proxima_ejecucion = Column(DateTime, nullable=False)

    # Indica si el recurrente está activo
    activo = Column(Boolean, default=True, nullable=False)

    # Claves foráneas
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)

    # Relaciones ORM
    usuario = relationship("Usuario", back_populates="recurrentes")
    categoria = relationship("Categoria")
    cuenta = relationship("Cuenta")