from datetime import datetime

from app.application.servicio_clientes import ServicioClientes
from app.domain.cliente import Cliente
from app.domain.errores import ApiPublicaNoDisponible
from app.infrastructure.memoria import RepositorioEnMemoria
from app.interfaces.api import crear_aplicacion

AHORA = datetime(2026, 10, 2, 8, 0)


class ApiPublicaFalsa:
    def __init__(self, orden: list[str] | None = None, falla: bool = False) -> None:
        self.llamadas: list[tuple] = []
        self._orden = orden
        self._falla = falla

    def crear(self, datos: dict) -> None:
        self._registrar("crear", datos)

    def actualizar(self, id_cliente: int, datos: dict) -> None:
        self._registrar("actualizar", id_cliente, datos)

    def eliminar(self, id_cliente: int) -> None:
        self._registrar("eliminar", id_cliente)

    def _registrar(self, *partes) -> None:
        if self._falla:
            raise ApiPublicaNoDisponible()
        self.llamadas.append(partes)
        if self._orden is not None:
            self._orden.append("api")


class RepositorioQueRegistra(RepositorioEnMemoria):
    def __init__(self, orden: list[str]) -> None:
        super().__init__()
        self._orden = orden

    def agregar(self, cliente: Cliente) -> None:
        self._orden.append("repositorio")
        super().agregar(cliente)

    def actualizar(self, cliente: Cliente) -> None:
        self._orden.append("repositorio")
        super().actualizar(cliente)


def servicio(api: ApiPublicaFalsa, repositorio, ids: list[int]) -> ServicioClientes:
    pendientes = iter(ids)

    def generar_id() -> int:
        return next(pendientes)

    return ServicioClientes(repositorio, api, generar_id, lambda: AHORA)


def cliente_guardado(repositorio: RepositorioEnMemoria, id_cliente: int = 7) -> Cliente:
    cliente = Cliente(id_cliente, "Ana Ruiz", "ana@ejemplo.com", "999", AHORA, 1)
    repositorio.agregar(cliente)
    return cliente


def aplicacion_de_prueba(servicio_clientes: ServicioClientes):
    return crear_aplicacion(servicio_clientes)
