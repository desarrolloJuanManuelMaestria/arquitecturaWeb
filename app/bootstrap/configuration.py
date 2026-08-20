"""
Validación de la configuración de la aplicación.
"""

from core.config.settings import settings


def validate_configuration() -> None:
    """
    Fuerza la carga de la configuración de la aplicación.

    Si durante la construcción de Settings ocurre un error,
    la aplicación no continuará iniciando.
    """

    _ = settings