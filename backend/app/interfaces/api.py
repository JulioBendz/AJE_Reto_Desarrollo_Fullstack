from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.application.servicio_clientes import ServicioClientes
from app.configuracion import origenes_permitidos
from app.domain.errores import (
    ApiPublicaNoDisponible,
    ClienteNoEncontrado,
    EmailDuplicado,
    IdNoDisponible,
)


class ClienteEntrada(BaseModel):
    nombres: str = Field(min_length=1, max_length=255)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=50)

    @field_validator("nombres")
    @classmethod
    def nombres_obligatorio(cls, valor: str) -> str:
        limpio = valor.strip()
        if not limpio:
            raise ValueError("El nombre es obligatorio")
        return limpio

    @field_validator("telefono")
    @classmethod
    def telefono_opcional(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        limpio = valor.strip()
        return limpio or None


class ClienteRespuesta(BaseModel):
    id: int
    nombres: str
    email: str
    telefono: str | None
    fecha_creacion: datetime
    estado: int


class IdRespuesta(BaseModel):
    id: int


class ErrorRespuesta(BaseModel):
    detalle: str


_errores = {
    400: {"model": ErrorRespuesta, "description": "Datos de entrada invalidos"},
    404: {"model": ErrorRespuesta, "description": "Cliente no encontrado"},
    409: {"model": ErrorRespuesta, "description": "El email ya esta registrado"},
    503: {"model": ErrorRespuesta, "description": "El API publica no esta disponible"},
}


def crear_aplicacion(servicio: ServicioClientes) -> FastAPI:
    aplicacion = FastAPI(
        title="API de clientes",
        version="1.0.0",
        description="CRUD de clientes. En alta, actualizacion y baja llama primero al API publica y despues persiste en PostgreSQL.",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=origenes_permitidos(),
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Accept"],
    )

    @aplicacion.exception_handler(RequestValidationError)
    async def entrada_invalida(_peticion, _error):
        return JSONResponse(status_code=400, content={"detalle": "Datos de entrada invalidos"})

    @aplicacion.exception_handler(ClienteNoEncontrado)
    async def no_encontrado(_peticion, _error):
        return JSONResponse(status_code=404, content={"detalle": "Cliente no encontrado"})

    @aplicacion.exception_handler(EmailDuplicado)
    async def email_duplicado(_peticion, _error):
        return JSONResponse(status_code=409, content={"detalle": "El email ya esta registrado"})

    @aplicacion.exception_handler(ApiPublicaNoDisponible)
    async def api_no_disponible(_peticion, _error):
        return JSONResponse(status_code=503, content={"detalle": "El API publica no esta disponible"})

    @aplicacion.exception_handler(IdNoDisponible)
    async def id_no_disponible(_peticion, _error):
        return JSONResponse(status_code=500, content={"detalle": "No se pudo generar el id del cliente"})

    @aplicacion.post(
        "/api/clientes",
        status_code=201,
        summary="Crear cliente",
        responses={codigo: _errores[codigo] for codigo in (400, 409, 503)},
    )
    def crear(entrada: ClienteEntrada) -> IdRespuesta:
        nuevo_id = servicio.crear(entrada.nombres, str(entrada.email), entrada.telefono)
        return IdRespuesta(id=nuevo_id)

    @aplicacion.get("/api/clientes", summary="Listar clientes activos")
    def listar() -> list[ClienteRespuesta]:
        return [_respuesta(cliente) for cliente in servicio.listar()]

    @aplicacion.get(
        "/api/clientes/{id_cliente}",
        summary="Obtener cliente por id",
        responses={404: _errores[404]},
    )
    def obtener(id_cliente: int) -> ClienteRespuesta:
        return _respuesta(servicio.obtener(id_cliente))

    @aplicacion.put(
        "/api/clientes/{id_cliente}",
        summary="Actualizar cliente",
        responses={codigo: _errores[codigo] for codigo in (400, 404, 409, 503)},
    )
    def actualizar(id_cliente: int, entrada: ClienteEntrada) -> ClienteRespuesta:
        cliente = servicio.actualizar(id_cliente, entrada.nombres, str(entrada.email), entrada.telefono)
        return _respuesta(cliente)

    @aplicacion.delete(
        "/api/clientes/{id_cliente}",
        status_code=204,
        summary="Eliminar cliente de forma logica",
        responses={codigo: _errores[codigo] for codigo in (404, 503)},
    )
    def eliminar(id_cliente: int) -> None:
        servicio.eliminar(id_cliente)

    def contrato_openapi():
        if aplicacion.openapi_schema:
            return aplicacion.openapi_schema
        esquema = get_openapi(
            title=aplicacion.title,
            version=aplicacion.version,
            description=aplicacion.description,
            routes=aplicacion.routes,
        )
        esquema["openapi"] = "3.0.3"
        aplicacion.openapi_schema = esquema
        return esquema

    aplicacion.openapi = contrato_openapi
    return aplicacion


def _respuesta(cliente) -> ClienteRespuesta:
    return ClienteRespuesta(
        id=cliente.id,
        nombres=cliente.nombres,
        email=cliente.email,
        telefono=cliente.telefono,
        fecha_creacion=cliente.fecha_creacion,
        estado=cliente.estado,
    )
