from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configuracion import url_base_de_datos

motor = create_engine(url_base_de_datos())
Sesion = sessionmaker(motor)
