# Modelo ORM de la categoría
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Categoria(Base):
    """
    Representa la tabla 'categorias' en la base de datos.
    Clasifica las transacciones del usuario (alimentación, ocio, transporte, etc.).
    Puede ser predefinida (id_usuario=None) o personalizada por el usuario.
    """

    __tablename__ = "categorias"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Nombre de la categoría (ej: Alimentación, Ocio, Transporte)
    nombre = Column(String(100), nullable=False)

    # Icono representativo de la categoría (ej: nombre de icono PrimeIcons)
    icono = Column(String(50), nullable=True)

    # Color asociado a la categoría en formato hexadecimal (ej: #FF5733)
    color = Column(String(7), nullable=True)

    # Tipo de categoría: 'ingreso' o 'gasto'
    tipo = Column(String(10), nullable=False)

    # Clave foránea al usuario propietario
    # nullable=True permite categorías predefinidas del sistema
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    # Relaciones ORM
    usuario = relationship("Usuario", back_populates="categorias")

    transacciones = relationship(
        "Transaccion",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )
    presupuestos = relationship(
        "Presupuesto",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )