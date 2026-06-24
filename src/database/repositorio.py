from sqlalchemy.orm import Session
from src.database.models import CarritoDB, ItemCarritoDB

class CarritoRepositorio:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_cart_if_not_exists(self, sesion_id: str) -> CarritoDB:
        cart = self.db.query(CarritoDB).filter(CarritoDB.sesion_id == sesion_id).first()
        if not cart:
            cart = CarritoDB(sesion_id=sesion_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def agregar_item(self, sesion_id: str, nombre: str, precio: float, cantidad: int) -> ItemCarritoDB:
        # Asegurar que el carrito exista
        cart = self.create_cart_if_not_exists(sesion_id)
        
        # Buscar si el item ya existe
        item = self.db.query(ItemCarritoDB).filter(
            ItemCarritoDB.carrito_id == cart.id,
            ItemCarritoDB.nombre == nombre
        ).first()
        
        if item:
            item.cantidad += cantidad
        else:
            item = ItemCarritoDB(carrito_id=cart.id, nombre=nombre, precio=precio, cantidad=cantidad)
            self.db.add(item)
            
        self.db.commit()
        self.db.refresh(item)
        return item

    def calcular_total(self, sesion_id: str) -> float:
        cart = self.db.query(CarritoDB).filter(CarritoDB.sesion_id == sesion_id).first()
        if not cart:
            return 0.0
            
        items = self.db.query(ItemCarritoDB).filter(ItemCarritoDB.carrito_id == cart.id).all()
        subtotal = sum(item.precio * item.cantidad for item in items)
        
        # Aplicar descuento si existe (asumimos porcentaje por defecto, o fijo)
        if cart.descuento_valor > 0:
            if cart.descuento_tipo == "porcentaje" or not cart.descuento_tipo:
                subtotal -= subtotal * (cart.descuento_valor / 100)
            elif cart.descuento_tipo == "fijo":
                subtotal -= cart.descuento_valor
                
        return max(0.0, subtotal)
