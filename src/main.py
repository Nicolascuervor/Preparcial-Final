from src.database.config import Base, engine
from src.carrito.api import app

# Las tablas serán creadas por los tests en la base de datos de prueba
# Base.metadata.create_all(bind=engine)

# app ya está definida en src.carrito.api
# uvicorn usará src.main:app
