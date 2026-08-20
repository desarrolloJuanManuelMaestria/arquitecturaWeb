"""
Configuración del endpoint GraphQL de la aplicación.

Este módulo expone el schema GraphQL mediante un endpoint HTTP.
La lógica de consultas y mutaciones pertenece al dominio GraphQL
de productos.
"""

from flask import Flask, jsonify, request

from services.products.graphql.schema import schema


def register_graphql(app: Flask) -> None:
    """
    Registra el endpoint GraphQL en la aplicación Flask.

    El endpoint recibe consultas GraphQL mediante solicitudes HTTP POST
    y las ejecuta utilizando el schema configurado.

    Args:
        app:
            Instancia de la aplicación Flask.
    """

    @app.route("/graphql", methods=["POST"])
    def graphql():
        """
        Ejecuta una consulta o mutación GraphQL.

        Returns:
            Respuesta HTTP con el resultado de GraphQL.
        """

        data = request.get_json()

        result = schema.execute(
            data.get("query"),
            variables=data.get("variables"),
        )

        response = {}

        if result.errors:
            response["errors"] = [
                str(error)
                for error in result.errors
            ]

        if result.data is not None:
            response["data"] = result.data

        status_code = 400 if result.errors else 200

        return jsonify(response), status_code