from datetime import datetime

from sqlalchemy import delete

from app.domain.cliente import Cliente
from app.domain.errores import EmailDuplicado
from app.infrastructure.base_de_datos import Sesion
from app.infrastructure.modelo_cliente import ClienteORM
from app.infrastructure.repositorio_sqlalchemy import RepositorioSqlAlchemy

AHORA = datetime(2026, 10, 2, 12, 0)
ID_PRUEBA = 910_000_001


def _limpiar() -> None:
    with Sesion() as sesion:
        sesion.execute(delete(ClienteORM).where(ClienteORM.id == ID_PRUEBA))
        sesion.commit()


def test_guarda_lee_actualiza_y_lista_en_postgres():
    repositorio = RepositorioSqlAlchemy(Sesion)
    _limpiar()
    try:
        repositorio.agregar(
            Cliente(ID_PRUEBA, "Ana Ruiz", "ana.orm@ejemplo.com", "999", AHORA, 1)
        )

        leido = repositorio.obtener(ID_PRUEBA)
        assert leido is not None
        assert leido.nombres == "Ana Ruiz"
        assert leido.email == "ana.orm@ejemplo.com"
        assert leido.estado == 1
        assert any(cliente.id == ID_PRUEBA for cliente in repositorio.listar_activos())

        leido.estado = 0
        repositorio.actualizar(leido)
        assert repositorio.obtener(ID_PRUEBA).estado == 0
        assert all(cliente.id != ID_PRUEBA for cliente in repositorio.listar_activos())
    finally:
        _limpiar()


def test_email_duplicado_en_postgres():
    repositorio = RepositorioSqlAlchemy(Sesion)
    _limpiar()
    try:
        repositorio.agregar(
            Cliente(ID_PRUEBA, "Ana Ruiz", "ana.orm@ejemplo.com", None, AHORA, 1)
        )
        try:
            repositorio.agregar(
                Cliente(ID_PRUEBA + 1, "Otra", "ana.orm@ejemplo.com", None, AHORA, 1)
            )
        except EmailDuplicado:
            return
        raise AssertionError("debio fallar")
    finally:
        with Sesion() as sesion:
            sesion.execute(
                delete(ClienteORM).where(ClienteORM.id.in_([ID_PRUEBA, ID_PRUEBA + 1]))
            )
            sesion.commit()
