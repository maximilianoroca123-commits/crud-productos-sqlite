from datetime import datetime
from config import RUTA_LOGS, RUTA_DB
import sqlite3

def conectar_db():
    return sqlite3.connect(RUTA_DB)

def crear_tablas(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        precio INTEGER,
        stock INTEGER
    )
    """)
    conexion.commit()

def registrar_log(mensaje):
    with open(RUTA_LOGS, "a") as archivo:
        archivo.write(f"{mostrar_hora()}: {mensaje} \n")

def mostrar_hora():
    hora_actual = datetime.now()
    hora_formateada = hora_actual.strftime(f"%d/%m/%Y - %H:%M:%S")
    return hora_formateada

def guardar_productos(conexion, productos):
    cursor = conexion.cursor()
    contador_guardados = 0

    for producto in productos:
        cursor.execute(
            """
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
            """,
            (
                producto["nombre"],
                producto["categoria"],
                producto["precio"],
                producto["stock"]
            )
        )
        contador_guardados += 1

    conexion.commit()
    return contador_guardados

def obtener_producto_por_nombre(conexion, nombre):

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM productos WHERE nombre = ?",
        (nombre,)
    )

    resultado = cursor.fetchone()

    return resultado