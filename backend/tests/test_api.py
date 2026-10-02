from fastapi.testclient import TestClient

from app.infrastructure.memoria import RepositorioEnMemoria
from tests.soporte import ApiPublicaFalsa, aplicacion_de_prueba, cliente_guardado, servicio


def cliente_http(ids: list[int], repositorio=None, falla: bool = False):
    repo = repositorio or RepositorioEnMemoria()
    aplicacion = aplicacion_de_prueba(servicio(ApiPublicaFalsa(falla=falla), repo, ids))
    return TestClient(aplicacion), repo


def test_post_devuelve_el_id_creado():
    cliente, _repositorio = cliente_http([15])

    respuesta = cliente.post("/api/clientes", json={"nombres": "Ana Ruiz", "email": "ana@ejemplo.com", "telefono": "999"})

    assert respuesta.status_code == 201
    assert respuesta.json() == {"id": 15}


def test_get_lista_y_get_por_id():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 4)
    cliente, _repositorio = cliente_http([], repositorio)

    lista = cliente.get("/api/clientes")
    uno = cliente.get("/api/clientes/4")
    falta = cliente.get("/api/clientes/50")

    assert lista.status_code == 200
    assert lista.json()[0]["id"] == 4
    assert uno.status_code == 200
    assert uno.json()["email"] == "ana@ejemplo.com"
    assert falta.status_code == 404


def test_put_y_delete():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 6)
    cliente, repo = cliente_http([], repositorio)

    actualizado = cliente.put("/api/clientes/6", json={"nombres": "Ana Actualizada", "email": "ana@ejemplo.com"})
    eliminado = cliente.delete("/api/clientes/6")
    consulta = cliente.get("/api/clientes/6")

    assert actualizado.status_code == 200
    assert actualizado.json()["nombres"] == "Ana Actualizada"
    assert eliminado.status_code == 204
    assert consulta.status_code == 404
    assert repo.obtener(6).estado == 0


def test_entrada_invalida_responde_400_y_no_llama_al_api():
    api = ApiPublicaFalsa()
    aplicacion = aplicacion_de_prueba(servicio(api, RepositorioEnMemoria(), [1]))
    cliente = TestClient(aplicacion)

    sin_nombre = cliente.post("/api/clientes", json={"nombres": "  ", "email": "ana@ejemplo.com"})
    sin_email = cliente.post("/api/clientes", json={"nombres": "Ana", "email": "no-es-email"})

    assert sin_nombre.status_code == 400
    assert sin_email.status_code == 400
    assert api.llamadas == []


def test_email_duplicado_responde_409():
    repositorio = RepositorioEnMemoria()
    cliente_guardado(repositorio, 1)
    cliente, _repositorio = cliente_http([2], repositorio)

    respuesta = cliente.post("/api/clientes", json={"nombres": "Otra", "email": "ana@ejemplo.com"})

    assert respuesta.status_code == 409


def test_el_contrato_es_openapi_3_y_swagger_lista_los_cinco_metodos():
    cliente, _repositorio = cliente_http([1])
    esquema = cliente.app.openapi()
    rutas = esquema["paths"]

    assert esquema["openapi"].startswith("3.0")
    assert cliente.app.docs_url == "/docs"
    assert set(rutas["/api/clientes"]) >= {"get", "post"}
    assert set(rutas["/api/clientes/{id_cliente}"]) >= {"get", "put", "delete"}


def test_api_publica_no_disponible_responde_503():
    cliente, repositorio = cliente_http([3], falla=True)

    respuesta = cliente.post("/api/clientes", json={"nombres": "Ana", "email": "ana@ejemplo.com"})

    assert respuesta.status_code == 503
    assert repositorio.obtener(3) is None
