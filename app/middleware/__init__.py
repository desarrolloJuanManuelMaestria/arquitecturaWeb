"""
Registro de middlewares de la aplicación.
"""

from flask import Flask


def register_middlewares(app: Flask) -> None:
    """
    Registra los middlewares de Flask.

    Args:
        app: Instancia de la aplicación Flask.
    """
    # Aquí agregaremos before_request, after_request, etc.
    pass