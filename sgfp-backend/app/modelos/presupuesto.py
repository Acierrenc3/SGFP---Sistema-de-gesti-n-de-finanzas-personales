# Modelo ORM del presupuesto
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Presupuesto(Base):
    """
    Representa la tabla 'presupuestos' en la base de datos.
    Define el límite mensual de gasto asignado a una categoría
    por el usuario.
    """

    __tablename__ = "presupuestos"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Importe máximo permitido para la categoría en el mes indicado
    importe_limite = Column(Float, nullable=False)

    # Mes al que corresponde el presupuesto (1-12)
    mes = Column(Integer, nullable=False)

    # Año al que corresponde el presupuesto (ej: 2025)
    anio = Column(Integer, nullable=False)

    # Clave foránea al usuario propietario
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Clave foránea a la categoría asociada
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # Relaciones ORM
    usuario = relationship("Usuario", back_populates="presupuestos")
    categoria = relationship("Categoria", back_populates="presupuestos")