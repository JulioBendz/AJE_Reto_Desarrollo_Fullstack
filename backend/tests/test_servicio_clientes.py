from app.domain.cliente import Cliente
from app.domain.errores import ClienteNoEncontrado, EmailDuplicado
from tests.soporte import (
    AHORA,
    ApiPublicaFalsa,
    RepositorioEnMemoria,
    RepositorioQueRegistra,
    cliente_guardado,
    servicio,
)


def test_crear_llama_al_api_publica_antes_de_guardar():
    orden = []
    api = ApiPublicaFalsa(orden)
    repositorio = RepositorioQueRegistra(orden)

    nuevo_id = servicio(api, repositorio, [41]).crear("Ana Ruiz", "ana@ejemplo.com", "999")

    assert nuevo_id == 41
    assert orden == ["api", "repositorio"]
    guardado = repositorio.obtener(41)
    assert guardado.nombres == "Ana Ruiz"
    assert guardado.email == "ana@ejemplo.com"
    assert guardado.telefono == "999"
    assert guardado.fecha_creacion == AHORA
    assert guardado.estado == 1
    assert api.llamadas == [("crear", {"nombres": "Ana Ruiz", "email": "ana@ejemplo.com", "telefono": "999"})]


def test_crear_genera_otro_id_si_el_primero_ya_existe():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 5)

    nuevo_id = servicio(ApiPublicaFalsa(), repositorio, [5, 9]).crear("Luis", "luis@ejemplo.com", None)

    assert nuevo_id == 9
    assert repositorio.obtener(9) is not None


def test_crear_no_guarda_si_el_api_publica_falla():
    repositorio = RepositorioEnMemoria()

    try:
        servicio(ApiPublicaFalsa(falla=True), repositorio, [3]).crear("Ana", "ana@ejemplo.com", None)
    except Exception as error:
        assert error.__class__.__name__ == "ApiPublicaNoDisponible"
    else:
        raise AssertionError("debio fallar")

    assert repositorio.obtener(3) is None


def test_listar_devuelve_solo_clientes_activos():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 1)
    inactivo = Cliente(2, "Luis", "luis@ejemplo.com", None, AHORA, 0)
    repositorio.agregar(inactivo)
    casos = servicio(ApiPublicaFalsa(), repositorio, [])

    assert [cliente.id for cliente in casos.listar()] == [1]


def test_obtener_por_id():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 4)

    obtenido = servicio(ApiPublicaFalsa(), repositorio, []).obtener(4)

    assert obtenido.email == "ana@ejemplo.com"


def test_obtener_inexistente_o_dado_de_baja():
    repositorio = RepositorioEnMemoria()
    inactivo = cliente_guardado(repositorio, 8)
    inactivo.estado = 0
    casos = servicio(ApiPublicaFalsa(), repositorio, [])

    for id_cliente in (99, 8):
        try:
            casos.obtener(id_cliente)
        except ClienteNoEncontrado:
            continue
        raise AssertionError("debio fallar")


def test_actualizar_llama_al_api_publica_antes_de_guardar():
    orden = []
    repositorio = RepositorioQueRegistra(orden)
    cliente_guardado(repositorio, 6)
    orden.clear()
    api = ApiPublicaFalsa(orden)

    actualizado = servicio(api, repositorio, []).actualizar(6, "Ana Actualizada", "ana@ejemplo.com", None)

    assert orden == ["api", "repositorio"]
    assert actualizado.nombres == "Ana Actualizada"
    assert api.llamadas[0][0] == "actualizar"
    assert api.llamadas[0][1] == 6


def test_eliminar_da_de_baja_sin_borrar_la_fila():
    orden = []
    repositorio = RepositorioQueRegistra(orden)
    cliente_guardado(repositorio, 6)
    orden.clear()
    api = ApiPublicaFalsa(orden)
    casos = servicio(api, repositorio, [])

    casos.eliminar(6)

    assert orden == ["api", "repositorio"]
    assert api.llamadas == [("eliminar", 6)]
    assert repositorio.obtener(6).estado == 0
    assert casos.listar() == []


def test_actualizar_y_eliminar_no_llaman_al_api_si_no_existe():
    api = ApiPublicaFalsa()
    casos = servicio(api, RepositorioEnMemoria(), [])

    for accion in (lambda: casos.actualizar(3, "Ana", "ana@ejemplo.com", None), lambda: casos.eliminar(3)):
        try:
            accion()
        except ClienteNoEncontrado:
            continue
        raise AssertionError("debio fallar")

    assert api.llamadas == []


def test_email_duplicado_al_crear():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 1)

    try:
        servicio(ApiPublicaFalsa(), repositorio, [2]).crear("Otra", "ana@ejemplo.com", None)
    except EmailDuplicado:
        return
    raise AssertionError("debio fallar")
