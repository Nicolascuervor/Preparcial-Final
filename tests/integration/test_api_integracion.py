import pytest
from src.database.models import CarritoDB, ItemCarritoDB

def test_agregar_producto_api(client, db_session):
    # Arrange
    session_id = "api-session-456"
    payload = {
        "nombre": "Mouse Inalámbrico",
        "precio": 50.0,
        "cantidad": 2
    }
    
    # Act
    response = client.post(f"/carrito/{session_id}/productos", json=payload)
    
    # Assert HTTP
    assert response.status_code == 201
    data = response.json()
    assert data["mensaje"] == "Producto agregado"
    assert "item_id" in data
    
    # Assert DB (Validar existencia real en Postgres después de la petición)
    carrito_en_db = db_session.query(CarritoDB).filter_by(sesion_id=session_id).first()
    assert carrito_en_db is not None
    
    item_en_db = db_session.query(ItemCarritoDB).filter_by(carrito_id=carrito_en_db.id).first()
    assert item_en_db is not None
    assert item_en_db.nombre == "Mouse Inalámbrico"
    assert item_en_db.cantidad == 2
