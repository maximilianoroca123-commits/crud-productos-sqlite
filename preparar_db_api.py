# Preparación de la base de la API y carga inicial si la tabla está vacía.

import sqlite3

from config import RUTA_DB_API
from persistencia import guardar_productos

productos_iniciales = [
    {
        "nombre": "Mouse",
        "categoria": "tecnologia",
        "precio": 8500,
        "stock": 7,
    },
    {
        "nombre": "teclado",
        "categoria": "tecnologia",
        "precio": 7500,
        "stock": 5,
    },
    {
        "nombre": "Pan",
        "categoria": "alimento",
        "precio": 7000,
        "stock": 12,
    },
]


# Define las restricciones para una base nueva de la API.
def crear_tabla_productos_api(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        precio INTEGER NOT NULL CHECK (precio > 0),
        stock INTEGER NOT NULL CHECK (stock >= 0)
        )
        """)
    conexion.commit()


# Este bloque se ejecuta al lanzar el script.
conexion = sqlite3.connect(RUTA_DB_API)
try:
    crear_tabla_productos_api(conexion)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS indice_productos_nombre_unico
        ON productos (LOWER(nombre))
        """)
    conexion.commit()
    cursor.execute("SELECT COUNT(*) FROM productos")
    fila = cursor.fetchone()
    total = fila[0]
    # No vuelve a cargar los ejemplos si ya hay productos.
    if total == 0:
        guardar_productos(conexion, productos_iniciales)
finally:
    conexion.close()
