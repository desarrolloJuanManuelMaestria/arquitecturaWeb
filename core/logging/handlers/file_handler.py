"""
Handler encargado de persistir logs en un archivo plano.
"""

from pathlib import Path
from typing import Any
from datetime import datetime

from core.logging.handlers.base_handler import BaseHandler


class FileHandler(BaseHandler):
    """
    Persistencia de logs en un archivo de texto.
    """

    def __init__(self, path: str) -> None:

        self._path = Path(path)

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        level: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """
        Escribe un evento en el archivo de log.
        """

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = (
            f"[{timestamp}] "
            f"[{level}] "
            f"{message}"
        )

        if data:
            line += f" | {data}"

        with self._path.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(line + "\n")