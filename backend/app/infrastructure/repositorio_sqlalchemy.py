from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.domain.cliente import Cliente
from app.domain.errores import EmailDuplicado
from app.infrastructure.modelo_cliente import ClienteORM


class RepositorioSqlAlchemy:
    def __init__(self, sesion: sessionmaker[Session]) -> None:
        self._sesion = sesion

    def obtener(self, id_cliente: int) -> Cliente | None:
        with self._sesion() as sesion:
            fila = sesion.get(ClienteORM, id_cliente)
            return None if fila is None else self._a_dominio(fila)

    def listar_activos(self) -> list[Cliente]:
        with self._sesion() as sesion:
            filas = sesion.query(ClienteORM).filter(ClienteORM.estado == 1).all()
            return [self._a_dominio(fila) for fila in filas]

    def agregar(self, cliente: Cliente) -> None:
        self._guardar(cliente, nuevo=True)

    def actualizar(self, cliente: Cliente) -> None:
        self._guardar(cliente, nuevo=False)

    def _guardar(self, cliente: Cliente, nuevo: bool) -> None:
        with self._sesion() as sesion:
            fila = ClienteORM(
                id=cliente.id,
                nombres=cliente.nombres,
                email=cliente.email,
                telefono=cliente.telefono,
                fecha_creacion=cliente.fecha_creacion,
                estado=cliente.estado,
            )
            try:
                if nuevo:
                    sesion.add(fila)
                else:
                    sesion.merge(fila)
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise EmailDuplicado() from error

    def _a_dominio(self, fila: ClienteORM) -> Cliente:
        return Cliente(
            id=fila.id,
            nombres=fila.nombres,
            email=fila.email,
            telefono=fila.telefono,
            fecha_creacion=fila.fecha_creacion,
            estado=fila.estado,
        )
