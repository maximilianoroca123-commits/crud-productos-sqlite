# Punto de entrada del CRUD de consola.

from menu import menu
from persistencia import conectar_db, crear_tablas

conexion = conectar_db()
crear_tablas(conexion)

menu(conexion)
