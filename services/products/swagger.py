"""
Especificaciones OpenAPI para el dominio de productos.

Este módulo contiene la documentación del API REST de productos.

La especificación se mantiene separada de las rutas para evitar
mezclar la implementación HTTP con la documentación de la API.

La documentación utiliza el formato Swagger 2.0, compatible con
Flasgger.
"""


# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------

PRODUCT_SCHEMA = {
    "type": "object",
    "description": "Representación de un producto.",
    "properties": {
        "id": {
            "type": "integer",
            "example": 2,
            "description": "Identificador único del producto.",
        },
        "nombre": {
            "type": "string",
            "example": "Teclado actualizado",
            "description": "Nombre del producto.",
        },
        "descripcion": {
            "type": "string",
            "example": "Teclado mecánico RGB",
            "description": "Descripción del producto.",
        },
        "precio": {
            "type": "number",
            "format": "float",
            "example": 150000,
            "description": "Precio del producto.",
        },
    },
}


PRODUCT_REQUEST_SCHEMA = {
    "type": "object",
    "description": "Datos necesarios para crear o actualizar un producto.",
    "required": [
        "nombre",
        "descripcion",
        "precio",
    ],
    "properties": {
        "nombre": {
            "type": "string",
            "example": "Monitor",
            "description": "Nombre del producto.",
        },
        "descripcion": {
            "type": "string",
            "example": "Monitor de 24 pulgadas",
            "description": "Descripción del producto.",
        },
        "precio": {
            "type": "number",
            "format": "float",
            "example": 850000,
            "description": "Precio del producto.",
        },
    },
}


PRODUCT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "integer",
            "example": 200,
        },
        "description": {
            "type": "string",
            "example": "Producto encontrado",
        },
        "data": {
            "type": "object",
            "properties": {
                "product": {
                    "$ref": "#/definitions/Product",
                },
            },
        },
    },
}


PRODUCT_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "integer",
            "example": 200,
        },
        "description": {
            "type": "string",
            "example": "Productos encontrados",
        },
        "data": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Product",
                    },
                },
            },
        },
    },
}


ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "integer",
            "example": 404,
        },
        "description": {
            "type": "string",
            "example": "Producto no encontrado",
        },
        "data": {
            "type": "object",
            "example": {},
        },
    },
}


DELETE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "integer",
            "example": 200,
        },
        "description": {
            "type": "string",
            "example": "Producto eliminado correctamente",
        },
        "data": {
            "type": "object",
            "example": {},
        },
    },
}


# ---------------------------------------------------------------------
# Definitions
# ---------------------------------------------------------------------

PRODUCT_DEFINITIONS = {
    "Product": PRODUCT_SCHEMA,
    "ProductRequest": PRODUCT_REQUEST_SCHEMA,
}


# ---------------------------------------------------------------------
# GET /products
# ---------------------------------------------------------------------

PRODUCTS_GET = {
    "tags": ["Products"],
    "summary": "Obtener todos los productos",
    "description": "Obtiene todos los productos registrados.",
    "definitions": PRODUCT_DEFINITIONS,
    "responses": {
        200: {
            "description": "Lista de productos encontrados.",
            "schema": PRODUCT_LIST_RESPONSE_SCHEMA,
        },
    },
}


# ---------------------------------------------------------------------
# GET /products/{product_id}
# ---------------------------------------------------------------------

PRODUCT_GET = {
    "tags": ["Products"],
    "summary": "Obtener un producto por ID",
    "description": "Obtiene un producto mediante su identificador.",
    "definitions": PRODUCT_DEFINITIONS,
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "description": "Identificador único del producto.",
            "type": "integer",
            "example": 2,
        },
    ],
    "responses": {
        200: {
            "description": "Producto encontrado.",
            "schema": PRODUCT_RESPONSE_SCHEMA,
        },
        404: {
            "description": "Producto no encontrado.",
            "schema": ERROR_RESPONSE_SCHEMA,
        },
    },
}


# ---------------------------------------------------------------------
# POST /products
# ---------------------------------------------------------------------

PRODUCT_CREATE = {
    "tags": ["Products"],
    "summary": "Crear un producto",
    "description": "Crea un nuevo producto.",
    "definitions": PRODUCT_DEFINITIONS,
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "description": "Datos del producto que será creado.",
            "schema": {
                "$ref": "#/definitions/ProductRequest",
            },
        },
    ],
    "responses": {
        201: {
            "description": "Producto creado correctamente.",
            "schema": PRODUCT_RESPONSE_SCHEMA,
        },
    },
}


# ---------------------------------------------------------------------
# PUT /products/{product_id}
# ---------------------------------------------------------------------

PRODUCT_UPDATE = {
    "tags": ["Products"],
    "summary": "Actualizar un producto",
    "description": "Actualiza un producto existente.",
    "definitions": PRODUCT_DEFINITIONS,
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "description": "Identificador único del producto.",
            "type": "integer",
            "example": 2,
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "description": "Datos actualizados del producto.",
            "schema": {
                "$ref": "#/definitions/ProductRequest",
            },
        },
    ],
    "responses": {
        200: {
            "description": "Producto actualizado correctamente.",
            "schema": PRODUCT_RESPONSE_SCHEMA,
        },
        404: {
            "description": "Producto no encontrado.",
            "schema": ERROR_RESPONSE_SCHEMA,
        },
    },
}


# ---------------------------------------------------------------------
# DELETE /products/{product_id}
# ---------------------------------------------------------------------

PRODUCT_DELETE = {
    "tags": ["Products"],
    "summary": "Eliminar un producto",
    "description": "Elimina un producto mediante su identificador.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "description": "Identificador único del producto.",
            "type": "integer",
            "example": 2,
        },
    ],
    "responses": {
        200: {
            "description": "Producto eliminado correctamente.",
            "schema": DELETE_RESPONSE_SCHEMA,
        },
        404: {
            "description": "Producto no encontrado.",
            "schema": ERROR_RESPONSE_SCHEMA,
        },
    },
}