"""
Este módulo configura e gerencia a conexão assíncrona com o banco de dados usando SQLAlchemy.
Ele define o mecanismo de banco de dados assíncrono, a fábrica de sessões e um gerenciador
de contexto para lidar com eventos de ciclo de vida do aplicativo FastAPI.

Funções:
    lifespan() -> AsyncGenerator[None, None]:
        Gerenciador de contexto assíncrono que lida com eventos de ciclo de vida do
        aplicativo FastAPI.
        Garante que o esquema do banco de dados seja criado no início do aplicativo.
    get_db() -> AsyncGenerator[AsyncSession, None]:
        Gerador assíncrono que fornece uma sessão de banco de dados.
"""
import os
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from web_app.db_models import User, BASE #pylint: disable=unused-import

__ENGINE = create_async_engine(f"postgresql+asyncpg://{os.getenv("POSTGRES_USER", "postgres")}:{ \
    os.getenv("POSTGRES_PASSWORD", "password")}@{os.getenv("POSTGRES_HOST", "localhost")}:{ \
    os.getenv("POSTGRES_PORT", "5432")}/{os.getenv("POSTGRES_DB", "postgres")}")

__SESSION = sessionmaker(__ENGINE, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app): # pylint: disable=unused-argument
    """
    Lifespan event handler for the FastAPI application.

    This function is an asynchronous context manager that handles the lifespan
    events of the FastAPI application. It ensures that the database schema is
    created at the start of the application by running the `create_all` method
    on the SQLAlchemy metadata.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    async with __ENGINE.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)
    yield


async def get_database():
    """
    Asynchronous generator function that provides a database session.

    Yields:
        session (AsyncSession): An asynchronous database session.
    """
    async with __SESSION() as session:
        yield session
