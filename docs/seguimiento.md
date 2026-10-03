# Seguimiento del reto

La especificación no se edita para anotar avance. La fuente es [reto-desarrollo-fullstack.md](spec/reto-desarrollo-fullstack.md). Este archivo es el único que se actualiza al cerrar un ítem.

Marca `[x]` solo cuando el ítem se puede demostrar (prueba en verde, contenedor levantado, pantalla usable o archivo entregable). Un ítem empezado sigue en `[ ]`.

El porcentaje es ítems marcados dividido entre ítems del checklist. Cada ítem pesa lo mismo. No hay nota por bloque: un bloque al 100 % no compensa otro en cero.

## Resumen


|        |     |
| ------ | --- |
| Ítems  | 25  |
| Hechos | 25  |
| Avance | 100 % |



| Bloque                 | Referencia                                                                                                                                                                                                                                                                                             | Ítems | Hechos |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----- | ------ |
| Datos                  | [§4.1](spec/reto-desarrollo-fullstack.md#41-base-de-datos)                                                                                                                                                                                                                                             | 2     | 2      |
| Backend                | [§4.2](spec/reto-desarrollo-fullstack.md#42-backend-en-nodejs-o-phyton), [§6.4](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [§6.5](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto)                                                                    | 7     | 7      |
| Integración            | [§4.3](spec/reto-desarrollo-fullstack.md#43-integración-api-pública-retoolcom), [§6.6](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto)                                                                                                                                           | 3     | 3      |
| Frontend               | [§4.4](spec/reto-desarrollo-fullstack.md#44-frontend), [§6.3](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto)                                                                                                                                                                    | 6     | 6      |
| Arquitectura y calidad | [§2](spec/reto-desarrollo-fullstack.md#2-objetivos-del-reto), [§6.1](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [§6.2](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [§6.7](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto) | 4     | 4      |
| Entorno y entrega      | [§6.8](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [§6.9](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [§7](spec/reto-desarrollo-fullstack.md#7-entregable)                                                                                       | 3     | 3      |




## Datos

Referencia: [§4.1](spec/reto-desarrollo-fullstack.md#41-base-de-datos) y [§5](spec/reto-desarrollo-fullstack.md#5-tecnologías-recomendadas).

- [x] PostgreSQL 17 o superior, con la base `retoDB`
- [x] Tabla `cliente` con `id`, `nombres`, `email`, `telefono`, `fecha_creacion` y `estado`, y las restricciones del spec



## Backend

Referencia: [§4.2](spec/reto-desarrollo-fullstack.md#42-backend-en-nodejs-o-phyton) y criterios [4](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto) y [5](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto).

- [x] `POST /api/clientes`: invoca el POST del API pública, persiste en `cliente`, genera el id con un entero aleatorio y lo retorna
- [x] `GET /api/clientes`: devuelve los clientes leídos desde PostgreSQL
- [x] `GET /api/clientes/:id`: devuelve un cliente por id
- [x] `PUT /api/clientes/:id`: invoca el PUT del API pública y actualiza la fila
- [x] `DELETE /api/clientes/:id`: invoca el DELETE del API pública y hace la baja lógica
- [x] Validación de entrada y códigos HTTP correctos
- [x] Contrato OpenAPI 3.0 publicado con Swagger



## Integración

Referencia: [§4.3](spec/reto-desarrollo-fullstack.md#43-integración-api-pública-retoolcom) y criterio [6](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto).

- [x] Recurso de prueba creado en Retool y su URL configurada en el backend
- [x] Cada `POST`, `PUT` y `DELETE` del backend llama al API pública antes de tocar la base
- [x] Circuit breaker en esa integración



## Frontend

Referencia: [§4.4](spec/reto-desarrollo-fullstack.md#44-frontend) y criterio [3](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto).

- [x] SPA en React 18 o superior, con React Router
- [x] Registro: formulario con validación, `POST` y listado actualizado con el alta
- [x] Consulta: listado con `GET` y acciones de editar y eliminar
- [x] Edición: `GET` por id, `PUT` y listado actualizado
- [x] Eliminación: `DELETE` y listado sin ese registro
- [x] Mensajes de éxito o fallo en las operaciones



## Arquitectura y calidad

Referencia: criterios [1](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), [2](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto) y [7](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto).

- [x] Frontend y backend organizados con Clean Architecture
- [x] Persistencia con un ORM sobre PostgreSQL
- [x] Pruebas unitarias en verde, con flujos de excepción, escritas al estilo TDD
- [x] SonarQube en el IDE y scanner con las métricas de calidad cumplidas



## Entorno y entrega

Referencia: criterios [8](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto) y [9](spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto), y [§7](spec/reto-desarrollo-fullstack.md#7-entregable).

- [x] `docker-compose` levanta frontend, backend y PostgreSQL
- [x] README con el procedimiento de instalación y ejecución
- [x] Zip de entrega con el nombre y el apellido



## Orden de trabajo

1. Stack fijado en [ADR 0001](adr/0001-stack-del-reto.md): React 18, React Router, Fetch API, FastAPI, Requests, Pycircuitbreaker, SQLAlchemy, PostgreSQL 17, Docker Compose, pytest y SonarQube. Sin librería de estilos hasta cerrar el checklist.
2. `docker-compose` con PostgreSQL y la tabla `cliente`.
3. Backend por TDD: pruebas de los cinco endpoints, luego Clean Architecture, validación y Swagger.
4. Cliente de Retool con circuit breaker, enganchado a `POST`, `PUT` y `DELETE`.
5. SPA: consulta, registro, edición y eliminación.
6. SonarQube, README de instalación y el zip de entrega.

