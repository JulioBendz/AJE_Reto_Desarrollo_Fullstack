from collections.abc import Callable
from datetime import datetime

from app.domain.cliente import Cliente
from app.domain.errores import ClienteNoEncontrado, IdNoDisponible
from app.application.puertos import ApiPublica, RepositorioClientes

ESTADO_ACTIVO = 1
ESTADO_INACTIVO = 0
INTENTOS_DE_ID = 20


class ServicioClientes:
    def __init__(
        self,
        repositorio: RepositorioClientes,
        api_publica: ApiPublica,
        generar_id: Callable[[], int],
        reloj: Callable[[], datetime],
    ) -> None:
        self._repositorio = repositorio
        self._api_publica = api_publica
        self._generar_id = generar_id
        self._reloj = reloj

    def crear(self, nombres: str, email: str, telefono: str | None) -> int:
        datos = self._datos(nombres, email, telefono)
        self._api_publica.crear(datos)
        cliente = Cliente(
            id=self._id_libre(),
            nombres=nombres,
            email=email,
            telefono=telefono,
            fecha_creacion=self._reloj(),
            estado=ESTADO_ACTIVO,
        )
        self._repositorio.agregar(cliente)
        return cliente.id

    def listar(self) -> list[Cliente]:
        return self._repositorio.listar_activos()

    def obtener(self, id_cliente: int) -> Cliente:
        return self._activo(id_cliente)

    def actualizar(self, id_cliente: int, nombres: str, email: str, telefono: str | None) -> Cliente:
        cliente = self._activo(id_cliente)
        datos = self._datos(nombres, email, telefono)
        self._api_publica.actualizar(cliente.email, datos)
        cliente.nombres = nombres
        cliente.email = email
        cliente.telefono = telefono
        self._repositorio.actualizar(cliente)
        return cliente

    def eliminar(self, id_cliente: int) -> None:
        cliente = self._activo(id_cliente)
        self._api_publica.eliminar(cliente.email)
        cliente.estado = ESTADO_INACTIVO
        self._repositorio.actualizar(cliente)

    def _activo(self, id_cliente: int) -> Cliente:
        cliente = self._repositorio.obtener(id_cliente)
        if cliente is None or cliente.estado != ESTADO_ACTIVO:
            raise ClienteNoEncontrado()
        return cliente

    def _id_libre(self) -> int:
        for _ in range(INTENTOS_DE_ID):
            candidato = self._generar_id()
            if self._repositorio.obtener(candidato) is None:
                return candidato
        raise IdNoDisponible()

    def _datos(self, nombres: str, email: str, telefono: str | None) -> dict:
        return {"nombres": nombres, "email": email, "telefono": telefono}
