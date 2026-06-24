import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from src.database.models import Base
from src.database.config import get_db
from src.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def engine(postgres_container):
    # Testcontainers usa psycopg2 por defecto, lo reemplazamos por psycopg (psycopg3) que es el que instalamos
    url = postgres_container.get_connection_url()
    url = url.replace("psycopg2", "psycopg")
    
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db_session(engine):
    """
    Implementación del Patrón Rollback.
    Se crea una transacción antes de la prueba y se hace rollback al final,
    sin importar si la prueba pasó o falló.
    """
    connection = engine.connect()
    transaction = connection.begin()
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture del TestClient que inyecta (override) la db_session transaccional
    para que la API utilice la misma base de datos de prueba y se le aplique el rollback.
    """
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
