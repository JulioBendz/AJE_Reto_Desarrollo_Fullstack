import requests
from pycircuitbreaker import CircuitBreaker

from app.domain.errores import ApiPublicaNoDisponible
from app.infrastructure import api_publica_retool
from app.infrastructure.api_publica_retool import ApiPublicaRetool


class Respuesta:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class RequestsFalso:
    def __init__(self, status_code: int = 201, fallar_red: bool = False) -> None:
        self.llamadas: list[tuple] = []
        self._status_code = status_code
        self._fallar_red = fallar_red

    def __call__(self, metodo, url, json=None, timeout=None):
        self.llamadas.append((metodo, url, json))
        if self._fallar_red:
            raise requests.ConnectionError("sin red")
        return Respuesta(self._status_code)


def _cliente(monkeypatch, red: RequestsFalso, umbral: int = 3) -> ApiPublicaRetool:
    monkeypatch.setattr(api_publica_retool.requests, "request", red)
    interruptor = CircuitBreaker(
        breaker_id=f"prueba-retool-{id(red)}",
        error_threshold=umbral,
        recovery_timeout=30,
        exception_denylist=(ApiPublicaNoDisponible,),
    )
    return ApiPublicaRetool("https://retoolapi.dev/recurso/clientes", interruptor)


def test_post_put_y_delete_usan_la_url_del_recurso(monkeypatch):
    red = RequestsFalso()
    cliente = _cliente(monkeypatch, red)

    cliente.crear({"nombres": "Ana"})
    cliente.actualizar(4, {"nombres": "Ana"})
    cliente.eliminar(4)

    assert red.llamadas[0][0:2] == ("POST", "https://retoolapi.dev/recurso/clientes")
    assert red.llamadas[1][0:2] == ("PUT", "https://retoolapi.dev/recurso/clientes/4")
    assert red.llamadas[2][0:2] == ("DELETE", "https://retoolapi.dev/recurso/clientes/4")


def test_el_circuito_se_abre_y_deja_de_llamar(monkeypatch):
    red = RequestsFalso(fallar_red=True)
    cliente = _cliente(monkeypatch, red, umbral=2)

    for _ in range(3):
        try:
            cliente.crear({})
        except ApiPublicaNoDisponible:
            continue
        raise AssertionError("debio fallar")

    assert len(red.llamadas) == 2
