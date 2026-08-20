"""
Schema GraphQL del dominio de productos.

Este módulo reúne las consultas, mutaciones y tipos GraphQL que
componen la API GraphQL de productos.

El schema representa el contrato que GraphQL expone a los clientes.
"""

import graphene

from services.products.graphql.mutations import ProductMutation
from services.products.graphql.queries import ProductQuery


class ProductSchema(
    ProductQuery,
    ProductMutation,
    graphene.ObjectType,
):
    """
    Schema GraphQL del dominio de productos.

    Agrupa las consultas y mutaciones disponibles para el dominio
    de productos.
    """

    pass


schema = graphene.Schema(
    query=ProductSchema,
    mutation=ProductSchema,
)