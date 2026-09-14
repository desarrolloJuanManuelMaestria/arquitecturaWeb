# Generated gRPC bindings for product.proto.

import grpc

from services.products.grpc.generated import product_pb2 as product__pb2


class ProductServiceStub:
    """Cliente gRPC para ProductService."""

    def __init__(self, channel):
        self.CreateProduct = channel.unary_unary(
            "/products.ProductService/CreateProduct",
            request_serializer=product__pb2.CreateProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.GetProduct = channel.unary_unary(
            "/products.ProductService/GetProduct",
            request_serializer=product__pb2.GetProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.ListProducts = channel.unary_unary(
            "/products.ProductService/ListProducts",
            request_serializer=product__pb2.Empty.SerializeToString,
            response_deserializer=product__pb2.ProductListResponse.FromString,
        )
        self.UpdateProduct = channel.unary_unary(
            "/products.ProductService/UpdateProduct",
            request_serializer=product__pb2.UpdateProductRequest.SerializeToString,
            response_deserializer=product__pb2.ProductResponse.FromString,
        )
        self.DeleteProduct = channel.unary_unary(
            "/products.ProductService/DeleteProduct",
            request_serializer=product__pb2.DeleteProductRequest.SerializeToString,
            response_deserializer=product__pb2.DeleteProductResponse.FromString,
        )
        self.WatchProducts = channel.unary_stream(
            "/products.ProductService/WatchProducts",
            request_serializer=product__pb2.WatchProductsRequest.SerializeToString,
            response_deserializer=product__pb2.ProductEvent.FromString,
        )


class ProductServiceServicer:
    """Contrato base del servidor ProductService."""

    def CreateProduct(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def GetProduct(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def ListProducts(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def UpdateProduct(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def DeleteProduct(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def WatchProducts(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_ProductServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateProduct": grpc.unary_unary_rpc_method_handler(
            servicer.CreateProduct,
            request_deserializer=product__pb2.CreateProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "GetProduct": grpc.unary_unary_rpc_method_handler(
            servicer.GetProduct,
            request_deserializer=product__pb2.GetProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "ListProducts": grpc.unary_unary_rpc_method_handler(
            servicer.ListProducts,
            request_deserializer=product__pb2.Empty.FromString,
            response_serializer=product__pb2.ProductListResponse.SerializeToString,
        ),
        "UpdateProduct": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateProduct,
            request_deserializer=product__pb2.UpdateProductRequest.FromString,
            response_serializer=product__pb2.ProductResponse.SerializeToString,
        ),
        "DeleteProduct": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteProduct,
            request_deserializer=product__pb2.DeleteProductRequest.FromString,
            response_serializer=product__pb2.DeleteProductResponse.SerializeToString,
        ),
        "WatchProducts": grpc.unary_stream_rpc_method_handler(
            servicer.WatchProducts,
            request_deserializer=product__pb2.WatchProductsRequest.FromString,
            response_serializer=product__pb2.ProductEvent.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "products.ProductService",
        rpc_method_handlers,
    )
    server.add_generic_rpc_handlers((generic_handler,))
