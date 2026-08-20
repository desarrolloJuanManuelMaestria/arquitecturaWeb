"""
Interfaz GraphiQL para explorar y probar la API GraphQL.

Este módulo expone una interfaz web para ejecutar queries y mutations
contra el endpoint GraphQL de la aplicación.

La interfaz GraphiQL se ejecuta en el navegador y utiliza el endpoint
`/graphql` de nuestra aplicación.
"""

from flask import Flask, render_template_string


GRAPHIQL_HTML = """
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>GraphiQL - Products API</title>

    <link
        rel="stylesheet"
        href="https://unpkg.com/graphiql@3.8.3/graphiql.min.css"
    >

    <style>
        html,
        body,
        #graphiql {
            height: 100%;
            margin: 0;
        }
    </style>
</head>

<body>

<div id="graphiql"></div>

<script
    crossorigin
    src="https://unpkg.com/react@18/umd/react.production.min.js">
</script>

<script
    crossorigin
    src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js">
</script>

<script
    crossorigin
    src="https://unpkg.com/graphiql@3.8.3/graphiql.min.js">
</script>

<script>
    const fetcher = GraphiQL.createFetcher({
        url: "/graphql"
    });

    const root = ReactDOM.createRoot(
        document.getElementById("graphiql")
    );

    root.render(
        React.createElement(GraphiQL, {
            fetcher: fetcher,
        })
    );
</script>

</body>

</html>
"""


def register_graphiql(app: Flask) -> None:
    """
    Registra la interfaz GraphiQL en la aplicación Flask.

    Args:
        app:
            Instancia de la aplicación Flask.
    """

    @app.route("/graphiql", methods=["GET"])
    def graphiql():
        """
        Muestra la interfaz GraphiQL.

        Returns:
            Página HTML de GraphiQL.
        """

        return render_template_string(GRAPHIQL_HTML)