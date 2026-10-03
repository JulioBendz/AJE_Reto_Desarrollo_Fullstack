from typing import Protocol

from app.domain.cliente import Cliente


class RepositorioClientes(Protocol):
    def obtener(self, id_cliente: int) -> Cliente | None:
        ...

    def listar_activos(self) -> list[Cliente]:
        ...

    def agregar(self, cliente: Cliente) -> None:
        ...

    def actualizar(self, cliente: Cliente) -> None:
        ...


class ApiPublica(Protocol):
    def crear(self, datos: dict) -> None:
        ...

    def actualizar(self, email_registrado: str, datos: dict) -> None:
        ...

    def eliminar(self, email_registrado: str) -> None:
        ...
