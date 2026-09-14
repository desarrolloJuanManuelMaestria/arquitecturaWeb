"""Manejadores globales de excepciones HTTP."""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from core.logging.logger_factory import get_logger
from services.products.exceptions import ProductValidationError
from shared.responses.response_builder import ResponseBuilder


logger = get_logger("application")


def _json_error(code: int, description: str):
    response = ResponseBuilder.build_response(
        code=code,
        description=description,
        data={},
    )
    return jsonify(response.to_dict()), response.code


def register_exception_handlers(app: Flask) -> None:
    """Registra los manejadores globales de excepciones."""

    @app.errorhandler(ProductValidationError)
    def handle_product_validation_error(exc: ProductValidationError):
        return _json_error(400, str(exc))

    @app.errorhandler(KeyError)
    def handle_missing_field(exc: KeyError):
        field = str(exc).strip("'")
        return _json_error(
            400,
            f"El campo '{field}' es obligatorio.",
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        return _json_error(
            exc.code or 500,
            exc.description,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        logger.exception("Error no controlado en la aplicación")
        return _json_error(
            500,
            "Ocurrió un error interno en la aplicación.",
        )
