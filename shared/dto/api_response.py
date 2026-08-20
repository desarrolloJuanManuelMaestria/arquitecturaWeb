"""
DTO que representa una respuesta estándar de la aplicación.

Este módulo define una estructura común para representar las respuestas
generadas por la aplicación. Permite mantener un formato consistente
para el código de respuesta, la descripción y los datos retornados.

El DTO es inmutable para evitar modificaciones accidentales después
de haber sido creado.
"""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ApiResponse:
    """
    Representa una respuesta estándar de la aplicación.

    Attributes:
        code: Código asociado al resultado de la operación.
        description: Descripción del resultado de la operación.
        data: Datos incluidos en la respuesta. Por defecto, contiene
            un diccionario vacío.
    """

    code: int
    description: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte la respuesta en un diccionario serializable.

        Returns:
            Diccionario que contiene el código, la descripción y los
            datos de la respuesta.
        """
        return asdict(self)