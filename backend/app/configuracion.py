from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def leer(nombre: str, defecto: str = "") -> str:
    return os.environ.get(nombre, defecto).strip()


def url_base_de_datos() -> str:
    url = leer("DATABASE_URL")
    if not url:
        raise RuntimeError("Define DATABASE_URL en backend/.env. La plantilla es backend/.env.example.")
    return url
