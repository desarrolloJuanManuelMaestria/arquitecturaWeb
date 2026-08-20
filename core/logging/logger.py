from typing import Any

from core.logging.handlers.base_handler import BaseHandler


class Logger:
    """
    Fachada para el sistema de logging.

    Delega la persistencia del evento al handler configurado.
    """

    def __init__(
        self,
        handler: BaseHandler,
    ) -> None:

        self._handler = handler

    def info(
        self,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:

        self._handler.write(
            level="INFO",
            message=message,
            data=data,
        )

    def warning(
        self,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:

        self._handler.write(
            level="WARNING",
            message=message,
            data=data,
        )

    def error(
        self,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:

        self._handler.write(
            level="ERROR",
            message=message,
            data=data,
        )