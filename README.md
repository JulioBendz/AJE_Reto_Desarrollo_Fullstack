# Reto de Desarrollo Fullstack

Aplicación CRUD de clientes con frontend React, backend, API pública de Retool y PostgreSQL. El alcance está cerrado en la especificación; el avance se anota aparte.

- Especificación: [docs/spec/reto-desarrollo-fullstack.md](docs/spec/reto-desarrollo-fullstack.md)
- Stack: [docs/adr/0001-stack-del-reto.md](docs/adr/0001-stack-del-reto.md)
- Seguimiento: [docs/seguimiento.md](docs/seguimiento.md)

Stack fijado: React 18, FastAPI, SQLAlchemy, Requests, Pycircuitbreaker, PostgreSQL 17 y Docker Compose.

## Base de datos local

Requiere Docker 22 o superior.

```bash
docker compose up -d
```

Eso crea la base `retoDB` y la tabla `cliente`. Usuario y contraseña locales: `postgres` / `postgres`. Puerto: `5432`.

```bash
docker compose exec postgres psql -U postgres -d retoDB -c "\d cliente"
```

La instalación y ejecución de frontend y backend se documentan aquí cuando existan.
