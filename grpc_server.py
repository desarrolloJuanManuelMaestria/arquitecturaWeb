"""Punto de entrada del servidor gRPC de productos."""

from concurrent import futures
import signal

import grpc
from grpc_reflection.v1alpha import reflection

from app.bootstrap import bootstrap
from core.config.settings import settings
from core.logging.logger_factory import get_logger
from services.products.grpc.generated import product_pb2, product_pb2_grpc
from services.products.grpc.product_grpc_service import ProductGrpcService


logger = get_logger("grpc")


def create_grpc_server() -> grpc.Server:
    """Crea y configura el servidor gRPC."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductGrpcService(),
        server,
    )

    service_names = (
        product_pb2.DESCRIPTOR.services_by_name["ProductService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port(f"[::]:{settings.grpc_port}")
    return server


def main() -> None:
    """Inicializa infraestructura y mantiene el servidor gRPC activo."""
    bootstrap()
    server = create_grpc_server()
    server.start()

    logger.info(
        "Servidor gRPC iniciado en el puerto %s",
        settings.grpc_port,
    )
    print(f"Servidor gRPC escuchando en 0.0.0.0:{settings.grpc_port}")

    def stop_server(*_args) -> None:
        logger.info("Deteniendo servidor gRPC...")
        server.stop(grace=5)

    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)

    server.wait_for_termination()


if __name__ == "__main__":
    main()
