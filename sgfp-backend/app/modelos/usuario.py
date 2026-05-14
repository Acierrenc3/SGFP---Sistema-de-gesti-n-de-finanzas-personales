# Modelo ORM del usuario
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Usuario(Base):
    """
    Representa la tabla 'usuarios' en la base de datos.
    Almacena las credenciales y preferencias de cada usuario registrado.
    """

    __tablename__ = "usuarios"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Nombre visible del usuario
    nombre = Column(String(100), nullable=False)

    # Email único usado para autenticación
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Hash bcrypt de la contraseña (nunca se almacena en texto plano)
    contrasena_hash = Column(String(255), nullable=False)

    # Moneda preferida del usuario (por defecto EUR)
    moneda = Column(String(10), nullable=False, default="EUR")

    # Zona horaria del usuario (por defecto Europe/Madrid)
    zona_horaria = Column(String(50), nullable=False, default="Europe/Madrid")

    # Indica si la cuenta está activa
    activo = Column(Boolean, default=True, nullable=False)

    # Relaciones ORM con otras tablas
    # cascade="all, delete-orphan" elimina los registros hijos al eliminar el usuario
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