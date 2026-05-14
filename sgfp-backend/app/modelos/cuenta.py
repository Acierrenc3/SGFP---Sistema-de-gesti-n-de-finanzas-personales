# Modelo ORM de la cuenta
# Basado en: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cuenta(Base):
    """
    Representa la tabla 'cuentas' en la base de datos.
    Almacena las fuentes de dinero del usuario
    (efectivo, cuenta bancaria, tarjeta, etc.).
    """

    __tablename__ = "cuentas"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Nombre descriptivo de la cuenta (ej: Cuenta corriente, Tarjeta Visa)
    nombre = Column(String(100), nullable=False)

    # Tipo de cuenta (ej: efectivo, bancaria, tarjeta, ahorro)
    tipo = Column(String(50), nullable=False)

    # Saldo inicial de la cuenta en el momento de su creación
    saldo_inicial = Column(Float, nullable=False, default=0.0)

    # Clave foránea al usuario propietario
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relaciones ORM
    usuario = relationship("Usuario", back_populates="cuentas")

    transacciones = relationship(
        "Transaccion",
        back_populates="cuenta",
        cascade="all, delete-orphan"
    )