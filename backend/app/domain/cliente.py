from dataclasses import dataclass
from datetime import datetime


@dataclass
class Cliente:
    id: int
    nombres: str
    email: str
    telefono: str | None
    fecha_creacion: datetime
    estado: int
