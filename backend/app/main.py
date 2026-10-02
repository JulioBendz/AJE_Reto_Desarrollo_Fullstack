from datetime import datetime
from random import randint

from app.application.servicio_clientes import ServicioClientes
from app.infrastructure.api_publica_retool import crear_api_publica
from app.infrastructure.base_de_datos import Sesion
from app.infrastructure.repositorio_sqlalchemy import RepositorioSqlAlchemy
from app.interfaces.api import crear_aplicacion


def generar_id_aleatorio() -> int:
    return randint(1, 2_147_483_647)


aplicacion = crear_aplicacion(
    ServicioClientes(
        RepositorioSqlAlchemy(Sesion),
        crear_api_publica(),
        generar_id_aleatorio,
        datetime.now,
    )
)
