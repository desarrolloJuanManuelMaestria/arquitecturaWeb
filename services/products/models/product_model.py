"""
Modelo ORM para la persistencia de productos.

Este módulo define la representación de un producto utilizada por
SQLAlchemy para interactuar con la tabla `products` de PostgreSQL.

El modelo pertenece a la capa de persistencia del dominio de productos
y utiliza la clase `Base` proporcionada por la infraestructura de base
de datos.
"""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base


class ProductModel(Base):
    """
    Representa un producto dentro del modelo de persistencia.

    Esta clase define la correspondencia entre los atributos de un
    producto y las columnas de la tabla `products` en PostgreSQL.

    Attributes:
        id: Identificador único del producto. Es la clave primaria y
            se genera automáticamente.
        nombre: Nombre del producto. Es obligatorio y admite hasta
            150 caracteres.
        descripcion: Descripción del producto. Es obligatoria y
            admite hasta 500 caracteres.
        precio: Precio del producto. Es obligatorio.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    precio: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )