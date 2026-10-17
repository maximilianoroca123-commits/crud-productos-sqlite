# Acceso a la base de la API y traducción de excepciones de SQLite.

import sqlite3

from config import RUTA_DB_API
from errores import ProductoDuplicadoError, ProductoNoEncontradoError, ErrorPersistencia
from logica_productos import construir_producto


# Abre la base de la API o traduce el fallo de conexión.
def conectar_db():
    try:
        return sqlite3.connect(RUTA_DB_API)
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo conectar con la base de datos") from error


# Convierte una fila SQL en un diccionario; conserva None.
def fila_a_producto(fila):
    if fila is None:
        return None
    nuevo_diccionario = {
        "id": fila[0],
        "nombre": fila[1],
        "categoria": fila[2],
        "precio": fila[3],
        "stock": fila[4],
    }
    return nuevo_diccionario


# Busca un producto por ID y devuelve None si no existe.
def obtener_producto_por_id(id):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        fila = cursor.fetchone()
        producto = fila_a_producto(fila)
        return producto
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo consultar el producto") from error
    finally:
        conexion.close()


# Compara el nombre en minúsculas antes de crear un producto.
def obtener_producto_por_nombre(nombre):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE LOWER(nombre) = ?", (nombre.lower(),)
        )
        fila = cursor.fetchone()
        producto = fila_a_producto(fila)
        return producto
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia(
            "No se pudo consultar el producto por nombre"
        ) from error
    finally:
        conexion.close()


# Devuelve todos los productos para consultas manuales.
def obtener_todos_los_productos():
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        productos = []
        for fila in filas:
            producto = fila_a_producto(fila)
            productos.append(producto)
        return productos
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo obtener los productos") from error
    finally:
        conexion.close()


# Inserta, confirma y recupera el ID generado por SQLite.
def crear_producto(nombre, categoria, precio, stock):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
                INSERT INTO productos (nombre, categoria, precio, stock)
                VALUES (?, ?, ?, ?)
                """,
            (nombre, categoria, precio, stock),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        producto = construir_producto(nuevo_id, nombre, categoria, precio, stock)
        return producto
    except sqlite3.IntegrityError as error:
        if "indice_productos_nombre_unico" in str(error):
            raise ProductoDuplicadoError("El producto ya existe") from error
        raise ErrorPersistencia(
            "Error interno, no se pudo realizar la operacion"
        ) from error
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo crear el producto") from error
    finally:
        conexion.close()


# Guarda precio y stock y comprueba que la fila exista.
def guardar_producto_actualizado(producto_actualizado):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
                UPDATE productos
                SET precio = ?, stock = ?
                WHERE id = ?
                """,
            (
                producto_actualizado["precio"],
                producto_actualizado["stock"],
                producto_actualizado["id"],
            ),
        )
        cantidad_filas = cursor.rowcount
        if cantidad_filas == 0:
            raise ProductoNoEncontradoError("Producto no encontrado")
        conexion.commit()
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo actualizar el producto") from error
    except sqlite3.IntegrityError as error:
        raise ErrorPersistencia(
            "Error interno, no se pudo realizar la operacion"
        ) from error
    finally:
        conexion.close()


# Elimina por ID y comprueba si se afectó alguna fila.
def eliminar_producto(id):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        cantidad_filas = cursor.rowcount
        if cantidad_filas == 0:
            raise ProductoNoEncontradoError("Producto no encontrado")
        conexion.commit()
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo eliminar el producto") from error
    finally:
        conexion.close()


# Filtra y ordena en SQL antes de aplicar LIMIT y OFFSET.
def obtener_productos_paginados(
    pagina,
    limite,
    categoria: str | None = None,
    precio_min: int | None = None,
    precio_max: int | None = None,
):
    offset = (pagina - 1) * limite
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
                SELECT id, nombre, categoria, precio, stock
                FROM productos
                WHERE (? IS NULL OR categoria = ?)
                AND (? IS NULL OR precio >= ?)
                AND (? IS NULL OR precio <= ?)
                ORDER BY id ASC
                LIMIT ? OFFSET ?
                """,
            (
                categoria,
                categoria,
                precio_min,
                precio_min,
                precio_max,
                precio_max,
                limite,
                offset,
            ),
        )
        filas = cursor.fetchall()
        productos = []
        for fila in filas:
            producto = fila_a_producto(fila)
            productos.append(producto)
        return productos
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo listar los productos") from error
    finally:
        conexion.close()


# Cuenta las coincidencias con los mismos filtros, sin paginación.
def contar_productos(
    categoria: str | None = None,
    precio_min: int | None = None,
    precio_max: int | None = None,
):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
                SELECT COUNT(*) FROM productos
                WHERE (? IS NULL OR categoria = ?)
                AND (? IS NULL OR precio >= ?)
                AND (? IS NULL OR precio <= ?)
                """,
            (categoria, categoria, precio_min, precio_min, precio_max, precio_max),
        )
        fila = cursor.fetchone()
        total = fila[0]
        return total
    except sqlite3.OperationalError as error:
        raise ErrorPersistencia("No se pudo contar los productos") from error
    finally:
        conexion.close()
