"""
Consultas GraphQL relacionadas con productos.

Este módulo define las operaciones de lectura disponibles en el
schema GraphQL.

Las consultas delegan la obtención de información en
`ProductService`. No acceden directamente al repositorio ni a la
base de datos.
"""

import graphene

from services.products.graphql.types import ProductType
from services.products.product_service import ProductService


class ProductQuery(graphene.ObjectType):
    """
    Define las consultas GraphQL disponibles para productos.
    """

    products = graphene.List(
        ProductType,
        description="Obtiene todos los productos registrados.",
    )

    product = graphene.Field(
        ProductType,
        id=graphene.Int(
            required=True,
            description="Identificador del producto.",
        ),
        description="Obtiene un producto mediante su identificador.",
    )

    def resolve_products(self, info):
        """
        Resuelve la consulta de todos los productos.

        Args:
            info:
                Información proporcionada por GraphQL durante la
                ejecución de la consulta.

        Returns:
            Lista de productos obtenida mediante ProductService.
        """
        service = ProductService()

        return service.get_all()

    def resolve_product(self, info, id):
        """
        Resuelve la consulta de un producto por identificador.

        Args:
            info:
                Información proporcionada por GraphQL durante la
                ejecución de la consulta.

            id:
                Identificador del producto.

        Returns:
            Producto encontrado o None si no existe.
        """
        service = ProductService()

        return service.get_by_id(id)