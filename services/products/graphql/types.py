"""
Tipos GraphQL relacionados con el dominio de productos.

Este módulo define cómo se representa un producto dentro del
schema GraphQL.

Los tipos GraphQL pertenecen a la capa de exposición GraphQL y
no reemplazan los modelos ni las entidades utilizadas por la
aplicación.
"""

import graphene


class ProductType(graphene.ObjectType):
    """
    Representa un producto dentro del schema GraphQL.
    """

    id = graphene.Int(
        description="Identificador único del producto."
    )

    nombre = graphene.String(
        description="Nombre del producto."
    )

    descripcion = graphene.String(
        description="Descripción del producto."
    )

    precio = graphene.Float(
        description="Precio del producto."
    )