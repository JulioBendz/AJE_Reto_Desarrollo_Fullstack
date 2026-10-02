from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def leer(nombre: str, defecto: str = "") -> str:
    return os.environ.get(nombre, defecto).strip()
