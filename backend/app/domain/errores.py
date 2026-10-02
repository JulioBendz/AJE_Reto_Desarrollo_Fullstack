class ErrorDeAplicacion(Exception):
    pass


class ClienteNoEncontrado(ErrorDeAplicacion):
    pass


class EmailDuplicado(ErrorDeAplicacion):
    pass


class ApiPublicaNoDisponible(ErrorDeAplicacion):
    pass


class IdNoDisponible(ErrorDeAplicacion):
    pass
