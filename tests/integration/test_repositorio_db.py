import pytest
from src.database.repositorio import CarritoRepositorio
from src.database.models import CarritoDB, ItemCarritoDB

def test_agregar_item_persiste_en_db(db_session):
    # Arrange
    repo = CarritoRepositorio(db_session)
    session_id = "test-session-123"
    
    # Act
    item = repo.agregar_item(session_id, "Laptop Gamer", 1500.0, 1)
    
    # Assert
    assert item.id is not None
    
    # Validar persistencia real consultando la base de datos a través de SQLAlchemy
    carrito_en_db = db_session.query(CarritoDB).filter_by(sesion_id=session_id).first()
    assert carrito_en_db is not None
    
    item_en_db = db_session.query(ItemCarritoDB).filter_by(carrito_id=carrito_en_db.id).first()
    assert item_en_db is not None
    assert item_en_db.nombre == "Laptop Gamer"
    assert item_en_db.precio == 1500.0
    assert item_en_db.cantidad == 1
