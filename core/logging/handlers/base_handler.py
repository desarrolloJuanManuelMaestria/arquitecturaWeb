"""
Define el contrato para todos los manejadores de logs.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseHandler(ABC):
    """
    Contrato base para los manejadores de logs.

    Toda implementación debe encargarse de persistir un evento
    utilizando el mecanismo que corresponda.
    """

    @abstractmethod
    def write(
        self,
        level: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """
        Persiste un evento de log.

        Args:
            level: Nivel del evento.
            message: Mensaje descriptivo.
            data: Información adicional.
        """
        raise NotImplementedError