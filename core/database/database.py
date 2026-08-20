from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config.settings import settings


class Base(DeclarativeBase):
    """Clase base para los modelos ORM."""


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def check_database_connection() -> None:
    """
    Verifica que la aplicación pueda establecer conexión
    con PostgreSQL.
    """
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def create_tables() -> None:
    """
    Crea las tablas definidas por los modelos ORM.
    """
    Base.metadata.create_all(bind=engine)