"""
Application Factory.

Punto de entrada para la creación de la aplicación Flask.
"""

from flask import Flask

from app.blueprint_registry import register_blueprints
from app.bootstrap import bootstrap
from app.exception_handlers import register_exception_handlers
from app.middleware import register_middlewares
from app.swagger import configure_swagger
from app.graphql import register_graphql
from app.graphiql import register_graphiql


def create_app() -> Flask:
    """
    Crea y configura la aplicación Flask.

    Returns:
        Instancia configurada de Flask.
    """
    
    app = Flask(__name__)
    
    bootstrap()
    
    configure_swagger(app)
    
    register_graphql(app)
    
    register_graphiql(app)

    register_middlewares(app)

    register_exception_handlers(app)

    register_blueprints(app)

    return app