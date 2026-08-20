"""
Repositorio para la gestión de productos.

Este módulo encapsula el acceso a los datos de productos mediante
SQLAlchemy. Su responsabilidad es realizar las operaciones de
persistencia y consulta sobre la tabla `products`.

El repositorio no conoce detalles de HTTP ni de Flask. Las operaciones
de negocio son coordinadas por `ProductService`.
"""

from sqlalchemy import select

from core.database.database import SessionLocal
from services.products.models.product_model import ProductModel


class ProductRepository:
    """
    Proporciona operaciones de persistencia para productos.

    Cada operación administra su propia sesión de SQLAlchemy, asegurando
    que la sesión se cierre automáticamente al finalizar la operación.
    """

    def create(self, product: ProductModel) -> ProductModel:
        """
        Persiste un nuevo producto en la base de datos.

        Args:
            product: Producto que será almacenado.

        Returns:
            El producto persistido, incluyendo el identificador generado
            por la base de datos.
        """
        with SessionLocal() as session:
            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    def get_all(self) -> list[ProductModel]:
        """
        Obtiene todos los productos almacenados.

        Returns:
            Lista de productos registrados en la base de datos.
        """
        with SessionLocal() as session:
            statement = select(ProductModel)
            result = session.scalars(statement)

            return list(result)

    def get_by_id(self, product_id: int) -> ProductModel | None:
        """
        Obtiene un producto mediante su identificador.

        Args:
            product_id: Identificador del producto que se desea consultar.

        Returns:
            El producto encontrado o None si no existe.
        """
        with SessionLocal() as session:
            return session.get(ProductModel, product_id)

    def update(
        self,
        product_id: int,
        nombre: str,
        descripcion: str,
        precio: float,
    ) -> ProductModel | None:
        """
        Actualiza los datos de un producto existente.

        Primero busca el producto mediante su identificador. Si existe,
        actualiza sus atributos y confirma los cambios en la base de datos.

        Args:
            product_id: Identificador del producto que se desea actualizar.
            nombre: Nuevo nombre del producto.
            descripcion: Nueva descripción del producto.
            precio: Nuevo precio del producto.

        Returns:
            El producto actualizado o None si no existe.
        """
        with SessionLocal() as session:
            product = session.get(ProductModel, product_id)

            if product is None:
                return None

            product.nombre = nombre
            product.descripcion = descripcion
            product.precio = precio

            session.commit()
            session.refresh(product)

            return product

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto mediante su identificador.

        Args:
            product_id: Identificador del producto que se desea eliminar.

        Returns:
            True si el producto fue eliminado correctamente o False
            si el producto no existe.
        """
        with SessionLocal() as session:
            product = session.get(ProductModel, product_id)

            if product is None:
                return False

            session.delete(product)
            session.commit()

            return True