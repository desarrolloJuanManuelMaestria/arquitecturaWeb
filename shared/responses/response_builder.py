"""
Construye respuestas estándar para la aplicación.

Este módulo proporciona una clase utilitaria para crear instancias de
`ApiResponse` con un formato uniforme para las respuestas de la
aplicación.
"""

from typing import Any

from shared.dto.api_response import ApiResponse


class ResponseBuilder:
    """
    Proporciona métodos para construir respuestas estándar de la
    aplicación.
    """

    @staticmethod
    def build_response(
        code: int,
        description: str,
        data: dict[str, Any],
    ) -> ApiResponse:
        """
        Construye una respuesta estándar de la aplicación.

        Args:
            code: Código HTTP asociado al resultado de la operación.
            description: Descripción del resultado de la operación.
            data: Información que será incluida en la respuesta.

        Returns:
            Instancia de `ApiResponse` con la información proporcionada.
        """
        return ApiResponse(
            code=code,
            description=description,
            data=data,
        )