"""
Configuración centralizada del sistema de logging.

Cada dominio de negocio posee su propio archivo de log con rotación
diaria y retención configurable.
"""

from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

from core.config.settings import settings
from typing import Dict

_loggers: Dict[str, logging.Logger] = {}


def get_logger(domain: str) -> logging.Logger:
    """
    Obtiene un logger para un dominio de negocio.

    Si el logger ya existe, reutiliza la instancia. En caso contrario,
    la crea y la configura automáticamente.

    Args:
        domain:
            Nombre del dominio (facturacion, nomina, seguridad, etc.).

    Returns:
        Instancia de logging.Logger.
    """

    if domain in _loggers:
        return _loggers[domain]

    logger = logging.getLogger(domain)

    logger.setLevel(
        getattr(
            logging,
            settings.log_level.upper(),
            logging.INFO,
        )
    )

    logger.propagate = False

    log_directory = Path(settings.log_path) / domain

    log_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = log_directory / f"{domain}.log"

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "[PID:%(process)d] | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=settings.log_retention_days,
        encoding="utf-8",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    _loggers[domain] = logger

    return logger