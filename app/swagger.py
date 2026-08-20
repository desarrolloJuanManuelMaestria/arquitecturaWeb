"""
Configuración de Swagger/OpenAPI para la aplicación.

Este módulo configura Flasgger para generar automáticamente la
documentación OpenAPI de los endpoints REST de la aplicación.
"""

from flasgger import Swagger


def configure_swagger(app) -> Swagger:
    """
    Configura Swagger para la aplicación Flask.

    Args:
        app: Instancia de la aplicación Flask.

    Returns:
        Instancia configurada de Swagger.
    """
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "openapi",
                "route": "/openapi.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "info": {
            "title": "Products API",
            "description": (
                "API REST para la gestión de productos."
            ),
            "version": "1.0.0",
        },
        "basePath": "/",
    }

    return Swagger(
        app,
        config=swagger_config,
        template=swagger_template,
    )