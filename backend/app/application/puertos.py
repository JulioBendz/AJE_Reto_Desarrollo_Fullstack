from typing import Protocol

from app.domain.cliente import Cliente


class RepositorioClientes(Protocol):
    def obtener(self, id_cliente: int) -> Cliente | None:
        pass

    def listar_activos(self) -> list[Cliente]:
        pass

    def agregar(self, cliente: Cliente) -> None:
        pass

    def actualizar(self, cliente: Cliente) -> None:
        pass


class ApiPublica(Protocol):
    def crear(self, datos: dict) -> None:
        pass

    def actualizar(self, id_cliente: int, datos: dict) -> None:
        pass

    def eliminar(self, id_cliente: int) -> None:
        pass
