"""
Bootstrap de la aplicación.

Coordina la inicialización de todos los componentes de infraestructura.
"""

from app.bootstrap.configuration import validate_configuration
from app.bootstrap.infrastructure import initialize_infrastructure


def bootstrap() -> None:
    """
    Inicializa la infraestructura de la aplicación.
    """

    validate_configuration()

    initialize_infrastructure()