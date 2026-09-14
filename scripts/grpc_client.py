"""Cliente de consola para probar el CRUD y el streaming gRPC."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import grpc

from services.products.grpc.generated import product_pb2, product_pb2_grpc


def product_to_text(product) -> str:
    return (
        f"id={product.id}, nombre={product.nombre!r}, "
        f"descripcion={product.descripcion!r}, precio={product.precio}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cliente gRPC de productos")
    parser.add_argument(
        "--target",
        default="localhost:50051",
        help="Servidor gRPC. Por defecto: localhost:50051",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="Lista todos los productos")

    get_parser = commands.add_parser("get", help="Consulta un producto")
    get_parser.add_argument("id", type=int)

    create_parser = commands.add_parser("create", help="Crea un producto")
    create_parser.add_argument("nombre")
    create_parser.add_argument("descripcion")
    create_parser.add_argument("precio", type=float)

    update_parser = commands.add_parser("update", help="Actualiza un producto")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("nombre")
    update_parser.add_argument("descripcion")
    update_parser.add_argument("precio", type=float)

    delete_parser = commands.add_parser("delete", help="Elimina un producto")
    delete_parser.add_argument("id", type=int)

    commands.add_parser(
        "watch",
        help="Escucha eventos de productos en tiempo real",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        with grpc.insecure_channel(args.target) as channel:
            stub = product_pb2_grpc.ProductServiceStub(channel)

            if args.command == "list":
                response = stub.ListProducts(product_pb2.Empty())
                for product in response.products:
                    print(product_to_text(product))
                return

            if args.command == "get":
                response = stub.GetProduct(
                    product_pb2.GetProductRequest(id=args.id)
                )
                print(response.message)
                print(product_to_text(response.product))
                return

            if args.command == "create":
                response = stub.CreateProduct(
                    product_pb2.CreateProductRequest(
                        nombre=args.nombre,
                        descripcion=args.descripcion,
                        precio=args.precio,
                    )
                )
                print(response.message)
                print(product_to_text(response.product))
                return

            if args.command == "update":
                response = stub.UpdateProduct(
                    product_pb2.UpdateProductRequest(
                        id=args.id,
                        nombre=args.nombre,
                        descripcion=args.descripcion,
                        precio=args.precio,
                    )
                )
                print(response.message)
                print(product_to_text(response.product))
                return

            if args.command == "delete":
                response = stub.DeleteProduct(
                    product_pb2.DeleteProductRequest(id=args.id)
                )
                print(response.message)
                return

            if args.command == "watch":
                print("Escuchando eventos. Ctrl+C para finalizar.")
                for event in stub.WatchProducts(
                    product_pb2.WatchProductsRequest()
                ):
                    event_name = product_pb2.ProductEventType.Name(event.type)
                    print(
                        f"{event_name} | {event.message} | "
                        f"{product_to_text(event.product)}"
                    )

    except grpc.RpcError as exc:
        print(f"gRPC {exc.code().name}: {exc.details()}")
        raise SystemExit(1) from exc
    except KeyboardInterrupt:
        print("\nCliente finalizado.")


if __name__ == "__main__":
    main()
