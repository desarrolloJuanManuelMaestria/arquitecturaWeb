# Arquitectura Web - Products API

API REST y GraphQL para la gestión de productos, desarrollada con Flask, SQLAlchemy y PostgreSQL.

El proyecto implementa una arquitectura organizada por responsabilidades, separando la capa HTTP, lógica de negocio, dominio, persistencia e infraestructura.

La aplicación está contenerizada mediante Docker y desplegada en Render, con integración continua mediante GitHub Actions.

---

## 🚀 Tecnologías

- Python 3.12
- Flask
- SQLAlchemy ORM
- PostgreSQL 16
- GraphQL
- Graphene
- GraphiQL
- Swagger / OpenAPI
- Gunicorn
- Docker
- Docker Compose
- GitHub Actions
- Render

---

## 🏗️ Arquitectura

La aplicación está organizada siguiendo una separación de responsabilidades por capas y dominios.

```text
crudArquitecturaWeb/
│
├── app/
│   ├── bootstrap/
│   │   ├── configuration.py
│   │   └── infrastructure.py
│   │
│   ├── middleware/
│   ├── blueprint_registry.py
│   ├── exception_handlers.py
│   ├── graphql.py
│   ├── graphiql.py
│   └── swagger.py
│
├── core/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── logging/
│   │   ├── handlers/
│   │   ├── logger.py
│   │   └── logger_factory.py
│   │
│   └── process/
│       └── process_result.py
│
├── services/
│   └── products/
│       ├── domain/
│       │   └── product.py
│       │
│       ├── graphql/
│       │   ├── mutations.py
│       │   ├── queries.py
│       │   ├── schema.py
│       │   └── types.py
│       │
│       ├── models/
│       │   └── product_model.py
│       │
│       ├── repositories/
│       │   └── product_repository.py
│       │
│       ├── product_service.py
│       ├── routes.py
│       └── swagger.py
│
├── shared/
│   ├── dto/
│   ├── exceptions/
│   └── responses/
│
├── Dockerfile
├── docker-compose.yml
├── graphql_test.py
├── requirements.txt
├── run.py
└── wsgi.py
```

---

## 🔄 Flujo de la aplicación

```text
HTTP Request
     │
     ▼
Flask Blueprint
     │
     ▼
Product Service
     │
     ▼
Product Repository
     │
     ▼
SQLAlchemy ORM
     │
     ▼
PostgreSQL
```

El servicio contiene la lógica de negocio y el repositorio es responsable del acceso a datos.

La capa HTTP no accede directamente a la base de datos.

---

## 📦 Funcionalidades

### REST API

La API permite:

- Consultar todos los productos.
- Consultar un producto por ID.
- Crear productos.
- Actualizar productos.
- Eliminar productos.

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/products` | Obtiene todos los productos |
| GET | `/products/{product_id}` | Obtiene un producto |
| POST | `/products` | Crea un producto |
| PUT | `/products/{product_id}` | Actualiza un producto |
| DELETE | `/products/{product_id}` | Elimina un producto |

---

# 🔷 GraphQL

El proyecto incorpora GraphQL utilizando Graphene.

### Endpoint

```text
/graphql
```

### GraphiQL

Para realizar consultas y mutaciones desde el navegador:

```text
/graphiql
```

### Ejemplo de consulta

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

### Ejemplo de mutación

```graphql
mutation {
  createProduct(
    nombre: "Mouse"
    descripcion: "Mouse inalámbrico"
    precio: 75000
  ) {
    id
    nombre
    precio
  }
}
```

GraphQL permite solicitar únicamente los campos requeridos por el consumidor.

---

# 📚 Swagger / OpenAPI

La documentación interactiva de la API REST está disponible mediante Swagger.

### Local

```text
http://localhost:5000/apidocs/
```

### Producción

```text
https://arquitectura-web-api.onrender.com/apidocs/
```

---

# 🐳 Ejecución con Docker

## Requisitos

- Docker
- Docker Compose

## Ejecutar el proyecto

Desde la raíz del proyecto:

```bash
docker compose up --build
```

La aplicación estará disponible en:

```text
http://localhost:5000
```

PostgreSQL estará disponible desde el host mediante:

```text
localhost:5433
```

La aplicación dentro de Docker utiliza:

```text
postgres:5432
```

como dirección del servidor PostgreSQL.

---

# ⚙️ Variables de entorno

Las variables utilizadas por la aplicación incluyen:

```env
DATABASE_URL=postgresql+psycopg://usuario:password@host/database
SERVER_ORIGIN=http://localhost:5000
LOG_PATH=logs
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30
```

Para desarrollo local se utiliza el archivo:

```text
.env
```

El archivo `.env` no debe ser versionado.

Se proporciona:

```text
.env.example
```

como referencia de configuración.

---

# 🗄️ Base de datos

La aplicación utiliza PostgreSQL y SQLAlchemy ORM.

La conexión se configura mediante:

```text
DATABASE_URL
```

Ejemplo:

```text
postgresql+psycopg://postgres:postgres@postgres:5432/products_db
```

Durante el proceso de inicialización de la aplicación se realiza:

1. Validación de configuración.
2. Verificación de conexión a PostgreSQL.
3. Creación de las tablas definidas por los modelos ORM.

---

# 🧪 Pruebas de GraphQL

Se incluye el archivo:

```text
graphql_test.py
```

que permite validar la ejecución del schema GraphQL directamente.

Ejemplo:

```bash
docker compose exec backend python graphql_test.py
```

---

# 🔁 Integración continua

El proyecto utiliza GitHub Actions para validar la aplicación automáticamente.

Flujo:

```text
git push
   │
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ├── Configuración de Python
   ├── Instalación de dependencias
   └── Validación de la aplicación
   │
   ▼
CI exitoso
```

El pipeline evita que cambios que no superen las validaciones continúen hacia el despliegue.

---

# ☁️ Despliegue

La aplicación está desplegada en Render utilizando Docker.

### Aplicación

```text
https://arquitectura-web-api.onrender.com
```

### Base de datos

El proyecto utiliza una instancia PostgreSQL administrada por Render.

La comunicación entre la aplicación y PostgreSQL utiliza la red interna de Render.

---

## 🚀 Flujo de despliegue

```text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ├─────────────────────┐
    │                     │
    ▼                     ▼
GitHub Actions          Render
    │                     │
    │ CI                  │ Docker Build
    ▼                     ▼
  PASS ───────────────► Deploy
                          │
                          ▼
                       Gunicorn
                          │
                          ▼
                        Flask
                          │
                          ▼
                      PostgreSQL
```

---

# 🔐 Configuración de producción

Las credenciales y secretos no se almacenan dentro del repositorio.

Las variables sensibles se configuran directamente en Render mediante Environment Variables.

La conexión de producción utiliza la URL interna de PostgreSQL proporcionada por Render.

---

# 📌 Estado del proyecto

Actualmente se encuentran implementados y validados:

- [x] API REST
- [x] CRUD de productos
- [x] Arquitectura por capas
- [x] Separación dominio / servicio / repositorio
- [x] SQLAlchemy ORM
- [x] PostgreSQL
- [x] Docker
- [x] Docker Compose
- [x] Swagger / OpenAPI
- [x] GraphQL
- [x] GraphiQL
- [x] GitHub Actions
- [x] Despliegue en Render
- [x] Conexión con PostgreSQL en producción
- [x] Validación de la aplicación en CI

---

# 👨‍💻 Autores

- Juan Manuel Gutierrez
- Juan Andres Duarte Niño
- Lily Johana Castillo Forero

Proyecto desarrollado como parte del proceso académico de formación en Arquitectura de Software.
