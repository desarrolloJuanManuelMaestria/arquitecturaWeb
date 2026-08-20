from core.database.database import (
    check_database_connection,
    create_tables,
)
from core.logging.logger_factory import get_logger
from shared.exceptions.bootstrap_exception import BootstrapException


logger = get_logger("infrastructure")


def initialize_infrastructure() -> None:
    """
    Inicializa y valida los componentes compartidos de la aplicación.
    """

    logger.info("Inicializando infraestructura...")

    try:
        check_database_connection()
        create_tables()

        logger.info(
            "Infraestructura inicializada correctamente."
        )

    except Exception as exc:
        logger.exception(
            "No fue posible inicializar la infraestructura."
        )

        raise BootstrapException(
            "No fue posible inicializar la infraestructura."
        ) from exc