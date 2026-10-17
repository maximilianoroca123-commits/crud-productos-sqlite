# Pruebas manuales del repositorio, sin pasar por HTTP.

from repositorio_sqlite import (
    obtener_producto_por_id,
    obtener_todos_los_productos,
    obtener_producto_por_nombre,
    crear_producto,
    conectar_db,
    guardar_producto_actualizado,
    eliminar_producto,
    obtener_productos_paginados,
    contar_productos,
)


def comprobar_nombres_duplicados():
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT LOWER(nombre), COUNT(*)
            FROM productos
            GROUP BY LOWER(nombre)
            HAVING COUNT(*) > 1
            """)
        resultados = cursor.fetchall()
        print(resultados)
    finally:
        conexion.close()


def comprobar_precios_y_stock():
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, precio, stock
            FROM productos
            WHERE precio IS NULL OR precio <= 0
            OR stock IS NULL OR stock < 0
            """)
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()


# print(comprobar_precios_y_stock())
# print(obtener_todos_los_productos())
# print(contar_productos())

# producto = crear_producto("Prueba despues de migracion", "tecnologia", 100, 0)
# print(producto)
# producto = obtener_producto_por_id(1)
# producto["precio"] = -1
# guardar_producto_actualizado(producto)
# print(obtener_producto_por_id(1))

# Ejemplos manuales: activar solo la prueba que se quiere ejecutar.
# crear_producto("MOUSE", "tecnologia", 9000, 1)
# producto = obtener_producto_por_id(4)
# print(producto)
# eliminar_producto(67)
# print(obtener_productos_paginados(1, 10, categoria="tecnologia", precio_max=8000))
# print (contar_productos())
