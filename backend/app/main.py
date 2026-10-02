from datetime import datetime
from random import randint

from app.application.servicio_clientes import ServicioClientes
from app.infrastructure.base_de_datos import Sesion
from app.infrastructure.repositorio_sqlalchemy import RepositorioSqlAlchemy
from app.interfaces.api import crear_aplicacion


class _ApiPublicaPendiente:
    def crear(self, datos: dict) -> None:
        return None

    def actualizar(self, id_cliente: int, datos: dict) -> None:
        return None

    def eliminar(self, id_cliente: int) -> None:
        return None


def generar_id_aleatorio() -> int:
    return randint(1, 2_147_483_647)


aplicacion = crear_aplicacion(
    ServicioClientes(
        RepositorioSqlAlchemy(Sesion),
        _ApiPublicaPendiente(),
        generar_id_aleatorio,
        datetime.now,
    )
)
