# Modelo ORM del usuario
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    moneda = Column(String(10), nullable=False, default="EUR")
    zona_horaria = Column(String(50), nullable=False, default="Atlantic/Canary")
    activo = Column(Boolean, default=True, nullable=False)

    transacciones = relationship(
        "Transaccion",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    categorias = relationship(
        "Categoria",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    presupuestos = relationship(
        "Presupuesto",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    cuentas = relationship(
        "Cuenta",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )