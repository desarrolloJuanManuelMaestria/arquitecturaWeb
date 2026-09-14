# Arquitectura Web - Products API

Backend para la gestión de productos desarrollado con **Flask**, **SQLAlchemy** y **PostgreSQL**. La solución expone la misma lógica de negocio mediante **REST**, **GraphQL** y **gRPC**.

Para la actividad de la **Unidad 4 - Arquitectura de Aplicaciones Web**, el foco está en la implementación y prueba del CRUD de `Producto` mediante **GraphQL** y **gRPC**, incluyendo manejo de errores y una demostración de comunicación en tiempo real mediante **server streaming**.

---

## Objetivo de la solución

La aplicación permite administrar productos con los siguientes atributos:

- `id`: identificador único.
- `nombre`: nombre del producto.
- `descripcion`: descripción del producto.
- `precio`: valor numérico del producto.

La lógica de negocio y el acceso a datos se reutilizan entre los diferentes mecanismos de comunicación. REST, GraphQL y gRPC no implementan CRUD independientes: todos delegan las operaciones a `ProductService`, que utiliza `ProductRepository` y SQLAlchemy para persistir la información en PostgreSQL.

---

## Tecnologías

- Python 3.12
- Flask
- SQLAlchemy ORM
- PostgreSQL 16
- GraphQL
- Graphene
- gRPC
- Protocol Buffers
- gRPC Server Streaming
- GraphiQL
- Swagger / OpenAPI
- Gunicorn
- Docker
- Docker Compose
- Render

---

## Arquitectura

```text
                         CLIENTES
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
        REST             GraphQL             gRPC
     /products          /graphql          :50051
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                     ProductService
                            │
                            ▼
                    ProductRepository
                            │
                            ▼
                      SQLAlchemy ORM
                            │
                            ▼
                       PostgreSQL
```

Esta organización mantiene separadas las responsabilidades de transporte, lógica de negocio y persistencia.

### Estructura principal

```text
crudArquitecturaWeb/
│
├── app/
│   ├── bootstrap/
│   ├── middleware/
│   ├── exception_handlers.py
│   ├── graphql.py
│   ├── graphiql.py
│   └── swagger.py
│
├── core/
│   ├── config/
│   ├── database/
│   ├── logging/
│   └── process/
│
├── services/
│   └── products/
│       ├── domain/
│       │   └── product.py
│       ├── models/
│       │   └── product_model.py
│       ├── repositories/
│       │   └── product_repository.py
│       ├── graphql/
│       │   ├── mutations.py
│       │   ├── queries.py
│       │   ├── schema.py
│       │   └── types.py
│       ├── grpc/
│       │   ├── proto/
│       │   │   └── product.proto
│       │   ├── generated/
│       │   │   ├── product_pb2.py
│       │   │   └── product_pb2_grpc.py
│       │   ├── event_broker.py
│       │   └── product_grpc_service.py
│       ├── exceptions.py
│       ├── product_service.py
│       └── routes.py
│
├── scripts/
│   ├── generate_grpc.py
│   └── grpc_client.py
│
├── docs/
│   └── U4_PRUEBAS.md
│
├── grpc_server.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── wsgi.py
```

---

# GraphQL

GraphQL está implementado con **Graphene** y reutiliza `ProductService` para ejecutar las operaciones sobre productos.

## Endpoint

```text
POST http://localhost:5000/graphql
```

## Interfaz GraphiQL

```text
http://localhost:5000/graphiql
```

## Operaciones implementadas

- Consultar todos los productos.
- Consultar un producto por ID.
- Crear un producto.
- Actualizar un producto.
- Eliminar un producto.

### Consultar productos

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

### Crear producto

```graphql
mutation {
  createProduct(
    nombre: "Mouse GraphQL"
    descripcion: "Producto creado mediante GraphQL"
    precio: 78000
  ) {
    id
    nombre
    descripcion
    precio
  }
}
```

### Actualizar producto

```graphql
mutation {
  updateProduct(
    id: 1
    nombre: "Mouse GraphQL Pro"
    descripcion: "Producto actualizado mediante GraphQL"
    precio: 95000
  ) {
    id
    nombre
    descripcion
    precio
  }
}
```

### Eliminar producto

```graphql
mutation {
  deleteProduct(id: 1)
}
```

GraphQL devuelve errores controlados cuando una operación no puede completarse; por ejemplo, cuando se consulta un producto inexistente.

---

# gRPC

El servicio gRPC utiliza **Protocol Buffers** para definir el contrato y expone el CRUD de productos en el puerto `50051`.

El contrato se encuentra en:

```text
services/products/grpc/proto/product.proto
```

## Métodos implementados

| RPC | Tipo | Descripción |
|---|---|---|
| `CreateProduct` | Unary | Crea un producto |
| `GetProduct` | Unary | Consulta un producto por ID |
| `ListProducts` | Unary | Lista todos los productos |
| `UpdateProduct` | Unary | Actualiza un producto |
| `DeleteProduct` | Unary | Elimina un producto |
| `WatchProducts` | Server streaming | Mantiene una conexión abierta y envía eventos de productos |

## Manejo de errores

El servicio utiliza códigos de estado gRPC para representar errores de forma explícita:

- `INVALID_ARGUMENT`: datos de entrada inválidos.
- `NOT_FOUND`: el producto solicitado no existe.
- `INTERNAL`: error inesperado del servidor.

Ejemplo esperado al consultar un producto eliminado o inexistente:

```text
gRPC NOT_FOUND: Producto con id 10 no encontrado.
```

---

## Comunicación en tiempo real con gRPC

Además del CRUD mediante llamadas unary, la solución incluye `WatchProducts`, implementado mediante **server streaming**.

```text
Cliente A                         Cliente B

WatchProducts()                  CreateProduct()
     │                                │
     │ stream abierto                 ▼
     │                         ProductService
     │                                │
     │                                ▼
     │                           PostgreSQL
     │                                │
     ◄──── PRODUCT_CREATED ───────────┘
```

El cliente suscrito puede recibir los siguientes eventos:

```text
PRODUCT_CREATED
PRODUCT_UPDATED
PRODUCT_DELETED
```

Ejemplo desde consola:

**Terminal 1**

```bash
python scripts/grpc_client.py watch
```

**Terminal 2**

```bash
python scripts/grpc_client.py create "Monitor Streaming" "Prueba comunicación tiempo real" 950000
```

La Terminal 1 recibe el evento de creación sin tener que realizar una nueva consulta.

> El broker de eventos utilizado para esta demostración se mantiene en memoria dentro del proceso gRPC. Por ello, `WatchProducts` recibe los cambios generados mediante el servicio gRPC. REST y GraphQL comparten la misma base de datos, pero no publican eventos en ese broker.

---

# REST y Swagger

REST se conserva como parte de la solución desarrollada previamente y comparte la misma capa de aplicación y persistencia.

## Endpoints REST

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/products` | Obtiene todos los productos |
| GET | `/products/{product_id}` | Obtiene un producto |
| POST | `/products` | Crea un producto |
| PUT | `/products/{product_id}` | Actualiza un producto |
| DELETE | `/products/{product_id}` | Elimina un producto |

Swagger está disponible localmente en:

```text
http://localhost:5000/apidocs/
```

---

# Base de datos y ORM

La aplicación utiliza **PostgreSQL** como base de datos relacional y **SQLAlchemy** como ORM.

La conexión se configura mediante:

```text
DATABASE_URL
```

En Docker Compose se utiliza:

```text
postgresql+psycopg://postgres:postgres@postgres:5432/products_db
```

La capa de servicios no ejecuta SQL manual. El acceso a los datos se realiza a través del repositorio y SQLAlchemy.

---

# Ejecución con Docker

## Requisitos

- Docker
- Docker Compose

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Validar los contenedores:

```bash
docker compose ps
```

Servicios esperados:

| Servicio | Dirección desde el host |
|---|---|
| Flask / REST / GraphQL / Swagger | `http://localhost:5000` |
| gRPC | `localhost:50051` |
| PostgreSQL | `localhost:5433` |

Dentro de la red de Docker, PostgreSQL se comunica por:

```text
postgres:5432
```

Para detener el ambiente:

```bash
docker compose down
```

---

# Variables de entorno

El proyecto incluye `.env.example` como referencia:

```env
FLASK_ENV=development
SERVER_ORIGIN=http://localhost:5000
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/products_db
GRPC_PORT=50051
LOG_PATH=logs
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30
```

El archivo `.env` real no debe versionarse ni contenerse en el repositorio.

---

# Pruebas de la Unidad 4

Las pruebas completas están documentadas en:

```text
docs/U4_PRUEBAS.md
```

La guía contiene:

- CRUD completo de GraphQL.
- CRUD completo de gRPC.
- Pruebas con `grpc_client.py`.
- Pruebas gRPC con Postman.
- Prueba de `WatchProducts` con server streaming.
- Validación de `NOT_FOUND`.
- Validación de `INVALID_ARGUMENT`.

Durante la validación local también se comprobó que un producto creado mediante gRPC puede ser consultado posteriormente mediante GraphQL, confirmando que ambos mecanismos utilizan la misma persistencia PostgreSQL.

---

# Regenerar código gRPC

Si se modifica `product.proto`, los bindings de Python pueden regenerarse con:

```bash
python scripts/generate_grpc.py
```

Los archivos generados se encuentran en:

```text
services/products/grpc/generated/
```

---

# Despliegue

La parte HTTP de la aplicación se encuentra preparada para ejecución mediante Gunicorn y Docker.

El despliegue existente en Render corresponde al servicio Flask que expone REST y GraphQL. El servicio gRPC se ejecuta como un proceso independiente y, para esta actividad, se demuestra localmente mediante Docker Compose en el puerto `50051`.

---

# Estado de implementación

| Componente | Estado |
|---|---|
| Entidad `Producto` | Implementado |
| SQLAlchemy ORM | Implementado |
| PostgreSQL | Implementado |
| CRUD GraphQL | Implementado y probado |
| Manejo de errores GraphQL | Implementado y probado |
| CRUD gRPC | Implementado y probado |
| Manejo de errores gRPC | Implementado y probado |
| `WatchProducts` server streaming | Implementado y probado |
| Docker / Docker Compose | Implementado y probado |
| REST / Swagger | Disponible como funcionalidad adicional |

---

# Contexto académico

Proyecto desarrollado como parte del proceso académico de formación en Arquitectura de Software.
