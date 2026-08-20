"""
Servicio de aplicación para la gestión de productos.

Este módulo coordina las operaciones relacionadas con productos y
delega la persistencia en `ProductRepository`.

El servicio no conoce detalles de HTTP ni de PostgreSQL. Su
responsabilidad es coordinar las operaciones que la aplicación
puede realizar sobre un producto y registrar los eventos relevantes
del dominio.
"""

from services.products.models.product_model import ProductModel
from services.products.repositories.product_repository import ProductRepository

from core.logging.logger_factory import get_logger


logger = get_logger("products")


class ProductService:
    """
    Coordina las operaciones de aplicación relacionadas con productos.

    El servicio utiliza `ProductRepository` para realizar las operaciones
    de persistencia y consulta, y registra los eventos relevantes mediante
    el sistema centralizado de logging.
    """

    def __init__(self):
        """
        Inicializa el servicio y su repositorio de productos.
        """
        self.repository = ProductRepository()

    def create(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
    ) -> ProductModel:
        """
        Crea un nuevo producto.

        Args:
            nombre: Nombre del producto.
            descripcion: Descripción del producto.
            precio: Precio del producto.

        Returns:
            El producto creado y persistido.
        """
        product = ProductModel(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
        )

        product = self.repository.create(product)

        logger.info(
            "Producto creado correctamente",
            extra={
                "product_id": product.id,
                "nombre": product.nombre,
            },
        )

        return product

    def get_all(self) -> list[ProductModel]:
        """
        Obtiene todos los productos.

        Returns:
            Lista de productos registrados.
        """
        products = self.repository.get_all()

        logger.info(
            "Consulta de productos realizada",
            extra={
                "count": len(products),
            },
        )

        return products

    def get_by_id(
        self,
        product_id: int,
    ) -> ProductModel | None:
        """
        Obtiene un producto mediante su identificador.

        Args:
            product_id: Identificador del producto.

        Returns:
            El producto encontrado o None si no existe.
        """
        product = self.repository.get_by_id(product_id)

        if product is None:
            logger.warning(
                "Producto no encontrado",
                extra={
                    "product_id": product_id,
                },
            )

            return None

        logger.info(
            "Producto consultado correctamente",
            extra={
                "product_id": product.id,
            },
        )

        return product

    def update(
        self,
        product_id: int,
        nombre: str,
        descripcion: str,
        precio: float,
    ) -> ProductModel | None:
        """
        Actualiza un producto existente.

        Args:
            product_id: Identificador del producto.
            nombre: Nuevo nombre del producto.
            descripcion: Nueva descripción del producto.
            precio: Nuevo precio del producto.

        Returns:
            El producto actualizado o None si no existe.
        """
        product = self.repository.update(
            product_id,
            nombre,
            descripcion,
            precio,
        )

        if product is None:
            logger.warning(
                "No fue posible actualizar el producto porque no existe",
                extra={
                    "product_id": product_id,
                },
            )

            return None

        logger.info(
            "Producto actualizado correctamente",
            extra={
                "product_id": product.id,
            },
        )

        return product

    def delete(
        self,
        product_id: int,
    ) -> bool:
        """
        Elimina un producto mediante su identificador.

        Args:
            product_id: Identificador del producto.

        Returns:
            True si el producto fue eliminado correctamente o False
            si no existe.
        """
        deleted = self.repository.delete(product_id)

        if not deleted:
            logger.warning(
                "No fue posible eliminar el producto porque no existe",
                extra={
                    "product_id": product_id,
                },
            )

            return False

        logger.info(
            "Producto eliminado correctamente",
            extra={
                "product_id": product_id,
            },
        )

        return True