import requests
from pycircuitbreaker import CircuitBreaker, CircuitBreakerException

from app.configuracion import leer
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

    def actualizar(self, email_registrado: str, datos: dict) -> None:
        id_externo = self._id_externo(email_registrado)
        self._enviar("PUT", f"{self._url_base}/{id_externo}", datos)

    def eliminar(self, email_registrado: str) -> None:
        id_externo = self._id_externo(email_registrado)
        self._enviar("DELETE", f"{self._url_base}/{id_externo}", None)

    def _id_externo(self, email: str) -> int:
        try:
            cuerpo = self._interruptor.call(lambda: self._peticion("GET", self._url_base, None, {"email": email}))
        except CircuitBreakerException as error:
            raise ApiPublicaNoDisponible() from error
        except ErrorDePeticionExterna as error:
            raise ApiPublicaNoDisponible() from error
        if not isinstance(cuerpo, list) or not cuerpo or "id" not in cuerpo[0]:
            raise ApiPublicaNoDisponible()
        return int(cuerpo[0]["id"])

    def _enviar(self, metodo: str, url: str, datos: dict | None) -> None:
        try:
            self._interruptor.call(lambda: self._peticion(metodo, url, datos))
        except CircuitBreakerException as error:
            raise ApiPublicaNoDisponible() from error
        except ErrorDePeticionExterna as error:
            raise ApiPublicaNoDisponible() from error

    def _peticion(self, metodo: str, url: str, datos: dict | None, params: dict | None = None):
        try:
            respuesta = requests.request(metodo, url, json=datos, params=params, timeout=5)
        except requests.RequestException as error:
            raise ApiPublicaNoDisponible() from error
        if respuesta.status_code >= 500:
            raise ApiPublicaNoDisponible()
        if respuesta.status_code >= 400:
            raise ErrorDePeticionExterna()
        if not respuesta.content:
            return None
        return respuesta.json()


class ApiPublicaSinConfigurar:
    def crear(self, datos: dict) -> None:
        raise ApiPublicaNoDisponible()

    def actualizar(self, email_registrado: str, datos: dict) -> None:
        raise ApiPublicaNoDisponible()

    def eliminar(self, email_registrado: str) -> None:
        raise ApiPublicaNoDisponible()


def crear_api_publica() -> ApiPublicaRetool | ApiPublicaSinConfigurar:
    url = leer("RETOOL_API_URL")
    if not url:
        return ApiPublicaSinConfigurar()
    return ApiPublicaRetool(url)
