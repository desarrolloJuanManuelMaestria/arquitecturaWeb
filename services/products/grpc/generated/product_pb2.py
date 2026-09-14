# -*- coding: utf-8 -*-
# Generated from services/products/grpc/proto/product.proto.
# Do not edit manually unless the .proto contract changes.

from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\x12\x08products"\x07\n\x05Empty"J\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\x13\n\x0bdescripcion\x18\x03 \x01(\t\x12\x0e\n\x06precio\x18\x04 \x01(\x01"K\n\x14CreateProductRequest\x12\x0e\n\x06nombre\x18\x01 \x01(\t\x12\x13\n\x0bdescripcion\x18\x02 \x01(\t\x12\x0e\n\x06precio\x18\x03 \x01(\x01"\x1f\n\x11GetProductRequest\x12\n\n\x02id\x18\x01 \x01(\x05"W\n\x14UpdateProductRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\x13\n\x0bdescripcion\x18\x03 \x01(\t\x12\x0e\n\x06precio\x18\x04 \x01(\x01""\n\x14DeleteProductRequest\x12\n\n\x02id\x18\x01 \x01(\x05"F\n\x0fProductResponse\x12"\n\x07product\x18\x01 \x01(\x0b2\x11.products.Product\x12\x0f\n\x07message\x18\x02 \x01(\t":\n\x13ProductListResponse\x12#\n\x08products\x18\x01 \x03(\x0b2\x11.products.Product"9\n\x15DeleteProductResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t"\x16\n\x14WatchProductsRequest"\x88\x01\n\x0cProductEvent\x12(\n\x04type\x18\x01 \x01(\x0e2\x1a.products.ProductEventType\x12"\n\x07product\x18\x02 \x01(\x0b2\x11.products.Product\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x19\n\x11timestamp_unix_ms\x18\x04 \x01(\x03*u\n\x10ProductEventType\x12"\n\x1ePRODUCT_EVENT_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fPRODUCT_CREATED\x10\x01\x12\x13\n\x0fPRODUCT_UPDATED\x10\x02\x12\x13\n\x0fPRODUCT_DELETED\x10\x032\xd5\x03\n\x0eProductService\x12L\n\rCreateProduct\x12\x1e.products.CreateProductRequest\x1a\x19.products.ProductResponse0\x00\x12F\n\nGetProduct\x12\x1b.products.GetProductRequest\x1a\x19.products.ProductResponse0\x00\x12@\n\x0cListProducts\x12\x0f.products.Empty\x1a\x1d.products.ProductListResponse0\x00\x12L\n\rUpdateProduct\x12\x1e.products.UpdateProductRequest\x1a\x19.products.ProductResponse0\x00\x12R\n\rDeleteProduct\x12\x1e.products.DeleteProductRequest\x1a\x1f.products.DeleteProductResponse0\x00\x12I\n\rWatchProducts\x12\x1e.products.WatchProductsRequest\x1a\x16.products.ProductEvent0\x01b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR,
    "services.products.grpc.generated.product_pb2",
    _globals,
)
