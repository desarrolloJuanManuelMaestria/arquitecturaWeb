"""
Mutaciones GraphQL relacionadas con productos.

Este módulo define las operaciones GraphQL que permiten crear,
actualizar y eliminar productos.

Las mutaciones delegan las operaciones al `ProductService`.
No acceden directamente al repositorio ni a la base de datos.
"""

import graphene

from services.products.graphql.types import ProductType
from services.products.product_service import ProductService


class CreateProduct(graphene.Mutation):
    """
    Mutation para crear un producto.
    """

    class Arguments:
        """
        Argumentos necesarios para crear un producto.
        """

        nombre = graphene.String(
            required=True,
            description="Nombre del producto.",
        )

        descripcion = graphene.String(
            required=True,
            description="Descripción del producto.",
        )

        precio = graphene.Float(
            required=True,
            description="Precio del producto.",
        )

    Output = ProductType

    def mutate(
        self,
        info,
        nombre: str,
        descripcion: str,
        precio: float,
    ):
        """
        Crea un producto mediante ProductService.

        Args:
            info:
                Información proporcionada por GraphQL.

            nombre:
                Nombre del producto.

            descripcion:
                Descripción del producto.

            precio:
                Precio del producto.

        Returns:
            Producto creado.
        """
        service = ProductService()

        return service.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
        )


class UpdateProduct(graphene.Mutation):
    """
    Mutation para actualizar un producto.
    """

    class Arguments:
        """
        Argumentos necesarios para actualizar un producto.
        """

        id = graphene.Int(
            required=True,
            description="Identificador del producto.",
        )

        nombre = graphene.String(
            required=True,
            description="Nuevo nombre del producto.",
        )

        descripcion = graphene.String(
            required=True,
            description="Nueva descripción del producto.",
        )

        precio = graphene.Float(
            required=True,
            description="Nuevo precio del producto.",
        )

    Output = ProductType

    def mutate(
        self,
        info,
        id: int,
        nombre: str,
        descripcion: str,
        precio: float,
    ):
        """
        Actualiza un producto mediante ProductService.

        Args:
            info:
                Información proporcionada por GraphQL.

            id:
                Identificador del producto.

            nombre:
                Nuevo nombre del producto.

            descripcion:
                Nueva descripción del producto.

            precio:
                Nuevo precio del producto.

        Returns:
            Producto actualizado o None si no existe.
        """
        service = ProductService()

        return service.update(
            product_id=id,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
        )


class DeleteProduct(graphene.Mutation):
    """
    Mutation para eliminar un producto.
    """

    class Arguments:
        """
        Argumentos necesarios para eliminar un producto.
        """

        id = graphene.Int(
            required=True,
            description="Identificador del producto.",
        )

    Output = graphene.Boolean

    def mutate(
        self,
        info,
        id: int,
    ):
        """
        Elimina un producto mediante ProductService.

        Args:
            info:
                Información proporcionada por GraphQL.

            id:
                Identificador del producto.

        Returns:
            True si el producto fue eliminado correctamente.
        """
        service = ProductService()

        return service.delete(id)


class ProductMutation(graphene.ObjectType):
    """
    Agrupa las mutaciones disponibles para productos.
    """

    create_product = CreateProduct.Field(
        description="Crea un nuevo producto."
    )

    update_product = UpdateProduct.Field(
        description="Actualiza un producto existente."
    )

    delete_product = DeleteProduct.Field(
        description="Elimina un producto."
    )