import os
import httpx

# Definimos la URL de la API. En un entorno Docker E2E, 
# puede venir por variable de entorno (ej: http://api:8000)
API_URL = os.getenv("API_URL", "http://localhost:8000")

def test_flujo_compra_e2e():
    """
    Escenario E2E: 
    1. Agrega dos productos diferentes a un carrito.
    2. Consulta el carrito.
    3. Valida suma matemática de los productos.
    """
    sesion_id = "cliente-e2e-101"
    
    # 1. Agrega el primer producto
    producto_1 = {
        "nombre": "Laptop Pro",
        "precio": 1200.0,
        "cantidad": 1
    }
    resp1 = httpx.post(f"{API_URL}/carrito/{sesion_id}/productos", json=producto_1)
    assert resp1.status_code == 201, f"Fallo al agregar producto 1: {resp1.text}"
    
    # 2. Agrega el segundo producto
    producto_2 = {
        "nombre": "Monitor 4K",
        "precio": 300.0,
        "cantidad": 2
    }
    resp2 = httpx.post(f"{API_URL}/carrito/{sesion_id}/productos", json=producto_2)
    assert resp2.status_code == 201, f"Fallo al agregar producto 2: {resp2.text}"
    
    # 3. Consulta el estado del carrito
    resp_get = httpx.get(f"{API_URL}/carrito/{sesion_id}")
    assert resp_get.status_code == 200, f"Fallo al consultar carrito: {resp_get.text}"
    
    datos_carrito = resp_get.json()
    
    # 4. Validar suma matemática (1200*1 + 300*2 = 1800)
    total_esperado = (producto_1["precio"] * producto_1["cantidad"]) + \
                     (producto_2["precio"] * producto_2["cantidad"])
                     
    assert datos_carrito["total"] == total_esperado
    assert datos_carrito["sesion_id"] == sesion_id
