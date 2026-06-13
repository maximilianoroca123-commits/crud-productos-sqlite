from persistencia import conectar_db, crear_tablas
from menu import menu

conexion = conectar_db()
crear_tablas(conexion)

menu(conexion)