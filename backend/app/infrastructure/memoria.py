from app.domain.cliente import Cliente
from app.domain.errores import EmailDuplicado


class RepositorioEnMemoria:
    def __init__(self) -> None:
        self._clientes: dict[int, Cliente] = {}

    def obtener(self, id_cliente: int) -> Cliente | None:
        return self._clientes.get(id_cliente)

    def listar_activos(self) -> list[Cliente]:
        return [cliente for cliente in self._clientes.values() if cliente.estado == 1]

    def agregar(self, cliente: Cliente) -> None:
        self._exigir_email_libre(cliente)
        self._clientes[cliente.id] = cliente

    def actualizar(self, cliente: Cliente) -> None:
        if self.obtener(cliente.id) is None:
            raise KeyError(cliente.id)
        self._exigir_email_libre(cliente)
        self._clientes[cliente.id] = cliente

    def _exigir_email_libre(self, cliente: Cliente) -> None:
        for guardado in self._clientes.values():
            if guardado.id != cliente.id and guardado.email == cliente.email:
                raise EmailDuplicado()
