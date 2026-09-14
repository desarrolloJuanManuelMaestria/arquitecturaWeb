"""Implementación gRPC del CRUD de productos y streaming de eventos."""

from __future__ import annotations

import time
from queue import Empty

import grpc

from core.logging.logger_factory import get_logger
from services.products.exceptions import ProductValidationError
from services.products.grpc.event_broker import product_event_broker
from services.products.grpc.generated import product_pb2, product_pb2_grpc
from services.products.product_service import ProductService


logger = get_logger("grpc")


class ProductGrpcService(product_pb2_grpc.ProductServiceServicer):
    """Expone las operaciones de ProductService mediante gRPC."""

    def __init__(self) -> None:
        self.service = ProductService()

    @staticmethod
    def _to_proto(product) -> product_pb2.Product:
        return product_pb2.Product(
            id=product.id,
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio=product.precio,
        )

    @staticmethod
    def _validate_id(product_id: int) -> None:
        if product_id <= 0:
            raise ProductValidationError(
                "El identificador del producto debe ser mayor que cero."
            )

    def _publish_event(self, event_type, product, message: str) -> None:
        product_event_broker.publish(
            product_pb2.ProductEvent(
                type=event_type,
                product=self._to_proto(product),
                message=message,
                timestamp_unix_ms=int(time.time() * 1000),
            )
        )

    def CreateProduct(self, request, context):
        try:
            product = self.service.create(
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
            )
        except ProductValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        except Exception as exc:
            logger.exception("Error creando producto mediante gRPC")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al crear el producto.",
            )

        self._publish_event(
            product_pb2.PRODUCT_CREATED,
            product,
            "Producto creado correctamente",
        )
        return product_pb2.ProductResponse(
            product=self._to_proto(product),
            message="Producto creado correctamente",
        )

    def GetProduct(self, request, context):
        try:
            self._validate_id(request.id)
            product = self.service.get_by_id(request.id)
        except ProductValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        except Exception:
            logger.exception("Error consultando producto mediante gRPC")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al consultar el producto.",
            )

        if product is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Producto con id {request.id} no encontrado.",
            )

        return product_pb2.ProductResponse(
            product=self._to_proto(product),
            message="Producto encontrado",
        )

    def ListProducts(self, request, context):
        try:
            products = self.service.get_all()
        except Exception:
            logger.exception("Error listando productos mediante gRPC")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al consultar los productos.",
            )

        return product_pb2.ProductListResponse(
            products=[self._to_proto(product) for product in products]
        )

    def UpdateProduct(self, request, context):
        try:
            self._validate_id(request.id)
            product = self.service.update(
                product_id=request.id,
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
            )
        except ProductValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        except Exception:
            logger.exception("Error actualizando producto mediante gRPC")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al actualizar el producto.",
            )

        if product is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Producto con id {request.id} no encontrado.",
            )

        self._publish_event(
            product_pb2.PRODUCT_UPDATED,
            product,
            "Producto actualizado correctamente",
        )
        return product_pb2.ProductResponse(
            product=self._to_proto(product),
            message="Producto actualizado correctamente",
        )

    def DeleteProduct(self, request, context):
        try:
            self._validate_id(request.id)
            product = self.service.get_by_id(request.id)
        except ProductValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        except Exception:
            logger.exception("Error consultando producto antes de eliminarlo")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al eliminar el producto.",
            )

        if product is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Producto con id {request.id} no encontrado.",
            )

        try:
            deleted = self.service.delete(request.id)
        except Exception:
            logger.exception("Error eliminando producto mediante gRPC")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "Ocurrió un error interno al eliminar el producto.",
            )

        if not deleted:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Producto con id {request.id} no encontrado.",
            )

        self._publish_event(
            product_pb2.PRODUCT_DELETED,
            product,
            "Producto eliminado correctamente",
        )
        return product_pb2.DeleteProductResponse(
            success=True,
            message="Producto eliminado correctamente",
        )

    def WatchProducts(self, request, context):
        """Mantiene el stream abierto y entrega eventos en tiempo real."""
        subscriber = product_event_broker.subscribe()
        logger.info("Cliente conectado al stream WatchProducts")

        try:
            while context.is_active():
                try:
                    yield subscriber.get(timeout=1)
                except Empty:
                    continue
        finally:
            product_event_broker.unsubscribe(subscriber)
            logger.info("Cliente desconectado del stream WatchProducts")
