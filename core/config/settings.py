"""
Centraliza la configuración de la aplicación.

Esta clase carga las variables de entorno una única vez y las expone
mediante propiedades de solo lectura.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Configuración global de la aplicación.

    Implementa el patrón Singleton para garantizar una única instancia
    durante el ciclo de vida de la aplicación.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()

        return cls._instance

    def _load(self) -> None:
        """
        Carga todas las variables de entorno.
        """

        self.server_origin = os.getenv(
            "SERVER_ORIGIN",
            "http://localhost:5000",
        )
        
        self.database_url = os.getenv("DATABASE_URL")
    
        
        self.log_path = os.getenv(
            "LOG_PATH",
            "logs",
        )

        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO",
        )

        self.log_retention_days = int(
            os.getenv(
                "LOG_RETENTION_DAYS",
                "30",
            )
        )


settings = Settings()