from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ClienteORM(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombres: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[int] = mapped_column(Integer, nullable=False)
