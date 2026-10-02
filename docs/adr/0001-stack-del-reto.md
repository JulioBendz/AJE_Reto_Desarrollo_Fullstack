# ADR 0001: Stack del reto

- Estado: Aceptado
- Fecha: 2026-10-02

## Contexto

El reto deja elegir el backend y el ORM dentro de una lista, y evalúa por separado OpenAPI 3.0 con Swagger, el circuit breaker, las pruebas y Docker. La fuente es [la especificación](../spec/reto-desarrollo-fullstack.md), secciones [3](../spec/reto-desarrollo-fullstack.md#3-componentes-del-reto), [5](../spec/reto-desarrollo-fullstack.md#5-tecnologías-recomendadas) y [6](../spec/reto-desarrollo-fullstack.md#6-criterios-de-evaluación-del-reto).

## Decisión

| Pieza | Elección | Por qué es la mejor opción dentro del reto |
|---|---|---|
| Frontend | React 18, React Router, Fetch API | La sección 3 fija React. La sección 5 pide la versión 18 o superior, React Router y Fetch API. |
| Backend | Python con FastAPI | Express, Flask y FastAPI están permitidos. FastAPI publica OpenAPI 3.0 y Swagger desde el código, que es el criterio 5 de evaluación. |
| Cliente HTTP | Requests | Es el cliente que la sección 5 nombra para Python. |
| Circuit breaker | Pycircuitbreaker | Es el circuit breaker que la sección 5 nombra para Python, y el patrón es el criterio 6. |
| ORM | SQLAlchemy | Un ORM es un objetivo del reto. SQLAlchemy es el que la sección 5 recomienda para Python. |
| Base de datos | PostgreSQL 17 | Es la versión de la sección 5. La base se llama `retoDB`. |
| Entorno | Docker 22 o superior y Docker Compose | Docker Compose con frontend, backend y PostgreSQL es el criterio 8. |
| Pruebas | pytest | El reto exige TDD y pruebas de excepciones. pytest es el ejecutor; no agrega funcionalidad. |
| Calidad | Plugin y scanner de SonarQube | Es el criterio 7. |
| Estilos | Ninguno al inicio | Bootstrap y Material UI son opcionales en la sección 5. |

Express con Sequelize, o Flask con SQLAlchemy, también cumplirían. Quedan descartados para no armar Swagger con librerías que el reto no nombra.

No entra ninguna herramienta fuera de esa lista hasta cerrar los 25 ítems de [seguimiento](../seguimiento.md).
