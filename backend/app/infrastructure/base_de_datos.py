from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configuracion import leer

URL_BASE_DE_DATOS = leer(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/retoDB",
)

motor = create_engine(URL_BASE_DE_DATOS)
Sesion = sessionmaker(motor)
