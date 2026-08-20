"""
Rutas HTTP para la gestión de productos.

Este módulo expone los endpoints REST relacionados con productos.
Su responsabilidad es recibir las solicitudes HTTP, delegar las
operaciones al `ProductService` y construir respuestas HTTP
estandarizadas mediante `ResponseBuilder`.

La lógica de negocio es responsabilidad del servicio y la persistencia
de los datos es responsabilidad del repositorio.
"""

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from services.products.product_service import ProductService
from services.products.swagger import (
    PRODUCTS_GET,
    PRODUCT_GET,
    PRODUCT_CREATE,
    PRODUCT_UPDATE,
    PRODUCT_DELETE,
)
from shared.responses.response_builder import ResponseBuilder


blueprint = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
)

product_service = ProductService()


def _product_to_dict(product) -> dict:
    """
    Convierte un producto en un diccionario serializable.

    Args:
        product: Producto que será convertido.

    Returns:
        Diccionario con los datos del producto.
    """
    return {
        "id": product.id,
        "nombre": product.nombre,
        "descripcion": product.descripcion,
        "precio": product.precio,
    }


@blueprint.route("", methods=["GET"])
@swag_from(PRODUCTS_GET)
def get_products():
    """
    Obtiene todos los productos registrados.
    """
    products = product_service.get_all()

    response = ResponseBuilder.build_response(
        code=200,
        description="Productos encontrados",
        data={
            "products": [
                _product_to_dict(product)
                for product in products
            ]
        },
    )

    return jsonify(response.to_dict()), response.code


@blueprint.route("/<int:product_id>", methods=["GET"])
@swag_from(PRODUCT_GET)
def get_product(product_id: int):
    """
    Obtiene un producto mediante su identificador.
    """
    product = product_service.get_by_id(product_id)

    if product is None:
        response = ResponseBuilder.build_response(
            code=404,
            description="Producto no encontrado",
            data={},
        )

        return jsonify(response.to_dict()), response.code

    response = ResponseBuilder.build_response(
        code=200,
        description="Producto encontrado",
        data={
            "product": _product_to_dict(product),
        },
    )

    return jsonify(response.to_dict()), response.code


@blueprint.route("", methods=["POST"])
@swag_from(PRODUCT_CREATE)
def create_product():
    """
    Crea un nuevo producto.
    """
    data = request.get_json()

    product = product_service.create(
        nombre=data["nombre"],
        descripcion=data["descripcion"],
        precio=data["precio"],
    )

    response = ResponseBuilder.build_response(
        code=201,
        description="Producto creado correctamente",
        data={
            "product": _product_to_dict(product),
        },
    )

    return jsonify(response.to_dict()), response.code


@blueprint.route("/<int:product_id>", methods=["PUT"])
@swag_from(PRODUCT_UPDATE)
def update_product(product_id: int):
    """
    Actualiza un producto existente.
    """
    data = request.get_json()

    product = product_service.update(
        product_id=product_id,
        nombre=data["nombre"],
        descripcion=data["descripcion"],
        precio=data["precio"],
    )

    if product is None:
        response = ResponseBuilder.build_response(
            code=404,
            description="Producto no encontrado",
            data={},
        )

        return jsonify(response.to_dict()), response.code

    response = ResponseBuilder.build_response(
        code=200,
        description="Producto actualizado correctamente",
        data={
            "product": _product_to_dict(product),
        },
    )

    return jsonify(response.to_dict()), response.code


@blueprint.route("/<int:product_id>", methods=["DELETE"])
@swag_from(PRODUCT_DELETE)
def delete_product(product_id: int):
    """
    Elimina un producto mediante su identificador.
    """
    deleted = product_service.delete(product_id)

    if not deleted:
        response = ResponseBuilder.build_response(
            code=404,
            description="Producto no encontrado",
            data={},
        )

        return jsonify(response.to_dict()), response.code

    response = ResponseBuilder.build_response(
        code=200,
        description="Producto eliminado correctamente",
        data={},
    )

    return jsonify(response.to_dict()), response.code