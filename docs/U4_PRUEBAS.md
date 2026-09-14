# Guía de pruebas - Unidad 4

Esta guía permite demostrar el CRUD completo con GraphQL y gRPC, además del streaming gRPC en tiempo real.

## 1. Levantar el ambiente

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Servicios esperados:

- REST / GraphQL / GraphiQL / Swagger: `http://localhost:5000`
- gRPC: `localhost:50051`
- PostgreSQL desde el host: `localhost:5433`

Validar contenedores:

```bash
docker compose ps
```

## 2. CRUD GraphQL

Abrir:

```text
http://localhost:5000/graphiql
```

### Crear

```graphql
mutation {
  createProduct(
    nombre: "Mouse"
    descripcion: "Mouse inalámbrico"
    precio: 75000
  ) {
    id
    nombre
    descripcion
    precio
  }
}
```

Guardar el `id` retornado para las siguientes pruebas.

### Consultar todos

```graphql
query {
  products {
    id
    nombre
    descripcion
    precio
  }
}
```

### Consultar por ID

```graphql
query {
  product(id: 1) {
    id
    nombre
    descripcion
    precio
  }
}
```

Cambiar `1` por el ID creado.

### Actualizar

```graphql
mutation {
  updateProduct(
    id: 1
    nombre: "Mouse Pro"
    descripcion: "Mouse inalámbrico actualizado"
    precio: 90000
  ) {
    id
    nombre
    descripcion
    precio
  }
}
```

### Eliminar

```graphql
mutation {
  deleteProduct(id: 1)
}
```

## 3. CRUD gRPC con Postman

En Postman crear una solicitud **gRPC** y usar:

```text
localhost:50051
```

El servidor tiene reflection habilitado. También se puede importar directamente:

```text
services/products/grpc/proto/product.proto
```

### CreateProduct

```json
{
  "nombre": "Teclado",
  "descripcion": "Teclado mecánico",
  "precio": 180000
}
```

### GetProduct

```json
{
  "id": 1
}
```

### ListProducts

```json
{}
```

### UpdateProduct

```json
{
  "id": 1,
  "nombre": "Teclado Pro",
  "descripcion": "Teclado mecánico actualizado",
  "precio": 210000
}
```

### DeleteProduct

```json
{
  "id": 1
}
```

## 4. Streaming gRPC en tiempo real

Abrir dos solicitudes gRPC en Postman.

### Ventana 1

Invocar:

```text
WatchProducts
```

Payload:

```json
{}
```

La solicitud queda abierta esperando eventos.

### Ventana 2

Invocar `CreateProduct`, `UpdateProduct` o `DeleteProduct`.

La ventana que está ejecutando `WatchProducts` recibirá inmediatamente uno de estos eventos:

```text
PRODUCT_CREATED
PRODUCT_UPDATED
PRODUCT_DELETED
```

Esto demuestra una conexión de server streaming mantenida en tiempo real entre cliente y servidor.

## 5. Prueba rápida desde consola

Escuchar eventos:

```bash
python scripts/grpc_client.py watch
```

En otra terminal crear un producto:

```bash
python scripts/grpc_client.py create "Monitor" "Monitor 24 pulgadas" 650000
```

Listar productos:

```bash
python scripts/grpc_client.py list
```

## 6. Manejo de errores

### Producto inexistente

Ejecutar `GetProduct` con un ID que no exista:

```json
{
  "id": 999999
}
```

Resultado esperado:

```text
NOT_FOUND
```

### Datos inválidos

Ejecutar `CreateProduct` con nombre vacío:

```json
{
  "nombre": "",
  "descripcion": "Prueba",
  "precio": 1000
}
```

Resultado esperado:

```text
INVALID_ARGUMENT
```

Estas pruebas cubren CRUD, ORM, manejo de errores y comunicación gRPC mediante streaming.
