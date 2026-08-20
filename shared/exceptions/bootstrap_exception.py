"""
Excepciones relacionadas con la inicialización de la aplicación.

Este módulo define las excepciones utilizadas durante el proceso de
inicialización de la infraestructura de la aplicación.
"""


class BootstrapException(Exception):
    """
    Representa un error ocurrido durante la inicialización de la
    infraestructura de la aplicación.

    Attributes:
        message: Descripción del error ocurrido.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            message: Descripción del error ocurrido.
        """
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """
        Obtiene la descripción del error.

        Returns:
            Mensaje asociado a la excepción.
        """
        return self.message