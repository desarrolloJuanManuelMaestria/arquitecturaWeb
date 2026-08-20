"""
Entidad de dominio que representa un producto.

Este módulo define la estructura básica de un producto dentro del
dominio de la aplicación. La entidad no depende de Flask, SQLAlchemy,
PostgreSQL ni de ningún componente de infraestructura.
"""

from dataclasses import dataclass


@dataclass
class Product:
    """
    Representa un producto dentro del dominio de la aplicación.

    Attributes:
        id: Identificador único del producto. Puede ser None cuando
            el producto todavía no ha sido persistido.
        nombre: Nombre del producto.
        descripcion: Descripción del producto.
        precio: Precio del producto.
    """

    id: int | None
    nombre: str
    descripcion: str
    precio: float