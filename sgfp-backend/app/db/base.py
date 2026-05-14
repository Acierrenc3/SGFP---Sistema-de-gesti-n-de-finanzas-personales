# Configuración de la base declarativa de SQLAlchemy
# Basado en: https://docs.sqlalchemy.org/en/20/orm/declarative_base.html

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base de la que heredarán todos los modelos SQLAlchemy.
    DeclarativeBase es la forma recomendada en SQLAlchemy 2.0
    para definir modelos ORM.
    """
    pass