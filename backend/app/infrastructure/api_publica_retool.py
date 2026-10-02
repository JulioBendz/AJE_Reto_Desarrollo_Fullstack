import os

import requests
from pycircuitbreaker import CircuitBreaker, CircuitBreakerException

from app.domain.errores import ApiPublicaNoDisponible


class ErrorDePeticionExterna(Exception):
    pass


class ApiPublicaRetool:
    def __init__(self, url_base: str, interruptor: CircuitBreaker | None = None) -> None:
        self._url_base = url_base.rstrip("/")
        self._interruptor = interruptor or CircuitBreaker(
            breaker_id="retool-clientes",
            error_threshold=3,
            recovery_timeout=30,
            exception_denylist=(ApiPublicaNoDisponible,),
        )

    def crear(self, datos: dict) -> None:
        self._enviar("POST", self._url_base, datos)

    def actualizar(self, id_cliente: int, datos: dict) -> None:
        self._enviar("PUT", f"{self._url_base}/{id_cliente}", datos)

    def eliminar(self, id_cliente: int) -> None:
        self._enviar("DELETE", f"{self._url_base}/{id_cliente}", None)

    def _enviar(self, metodo: str, url: str, datos: dict | None) -> None:
        try:
            self._interruptor.call(lambda: self._peticion(metodo, url, datos))
        except CircuitBreakerException as error:
            raise ApiPublicaNoDisponible() from error
        except ErrorDePeticionExterna as error:
            raise ApiPublicaNoDisponible() from error

    def _peticion(self, metodo: str, url: str, datos: dict | None) -> None:
        try:
            respuesta = requests.request(metodo, url, json=datos, timeout=5)
        except requests.RequestException as error:
            raise ApiPublicaNoDisponible() from error
        if respuesta.status_code >= 500:
            raise ApiPublicaNoDisponible()
        if respuesta.status_code >= 400:
            raise ErrorDePeticionExterna()


class ApiPublicaSinConfigurar:
    def crear(self, datos: dict) -> None:
        raise ApiPublicaNoDisponible()

    def actualizar(self, id_cliente: int, datos: dict) -> None:
        raise ApiPublicaNoDisponible()

    def eliminar(self, id_cliente: int) -> None:
        raise ApiPublicaNoDisponible()


def crear_api_publica() -> ApiPublicaRetool | ApiPublicaSinConfigurar:
    url = os.environ.get("RETOOL_API_URL", "").strip()
    if not url:
        return ApiPublicaSinConfigurar()
    return ApiPublicaRetool(url)
