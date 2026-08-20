"""
Registro automático de Blueprints.

Descubre todos los módulos `routes.py` dentro del directorio `services`
y registra el Blueprint expuesto como `blueprint`.
"""

from importlib import import_module
from pathlib import Path

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """
    Descubre y registra automáticamente los Blueprints de todos los
    dominios de negocio.

    Args:
        app: Instancia de la aplicación Flask.
    """

    services_path = Path(__file__).resolve().parent.parent / "services"

    for service in services_path.iterdir():

        if not service.is_dir():
            continue

        routes_file = service / "routes.py"

        if not routes_file.exists():
            continue

        module = import_module(
            f"services.{service.name}.routes"
        )

        blueprint = getattr(module, "blueprint", None)

        if blueprint is not None:
            app.register_blueprint(blueprint)