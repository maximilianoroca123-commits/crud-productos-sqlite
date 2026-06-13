from config import CATEGORIAS_VALIDAS
from validaciones import pedir_opcion, pedir_numero, solicitar_nombre, solicitar_id
from busqueda import obtener_producto_por_id, obtener_producto_por_nombre


def crear_producto(nombre_producto):
    categoria_producto = pedir_opcion(
        "Ingrese categoria del producto: ",
        CATEGORIAS_VALIDAS
    )

    precio_producto = pedir_numero("Ingrese el precio del producto: ")
    stock_producto = pedir_numero("Ingrese el stock del producto: ")

    producto = {
        "nombre": nombre_producto,
        "categoria": categoria_producto,
        "precio": precio_producto,
        "stock": stock_producto
    }

    return producto

def registrar_producto(conexion):
    nombre = solicitar_nombre()
    producto_existente = obtener_producto_por_nombre(conexion, nombre)
    if producto_existente is not None:
        return None
    nuevo_producto = crear_producto(nombre)
    cursor = conexion.cursor()
    cursor.execute(
    """
    INSERT INTO productos (nombre, categoria, precio, stock)
    VALUES (?, ?, ?, ?)
    """,
    (nuevo_producto["nombre"], nuevo_producto["categoria"], nuevo_producto["precio"], nuevo_producto["stock"])
)
    nuevo_producto["id"] = cursor.lastrowid
    conexion.commit()
    return nuevo_producto


def eliminar_producto(conexion):
    id_producto = solicitar_id()
    producto_existente = obtener_producto_por_id(conexion, id_producto)

    if producto_existente is None:
        return None
    
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM productos WHERE id = ?",
        (id_producto,)
    )
    conexion.commit()

    return producto_existente


def actualizar_producto(conexion):
    id_producto = solicitar_id()
    producto = obtener_producto_por_id(conexion, id_producto)
    modificado = False
    if producto is None:
        return None

    print("1. Actualizar producto")
    print("2. Cancelar")

    opcion = pedir_opcion("Ingrese una opcion: ", ["1", "2"])

    if opcion == "1":
        cursor = conexion.cursor()
        nuevo_precio = pedir_opcion("Desea actualizar el precio?: ", ["si", "no"])

        if nuevo_precio == "si":
            precio_actualizado = pedir_numero("Ingrese nuevo precio: ")
            cursor.execute("""UPDATE productos
                           SET precio = ?
                           WHERE id = ?""",
                           (precio_actualizado, id_producto)
                           )
            modificado = True

        nuevo_stock = pedir_opcion("Desea actualizar el stock?: ", ["si", "no"])

        if nuevo_stock == "si":
            stock_actualizado = pedir_numero("Ingrese nuevo stock: ")
            cursor.execute("""UPDATE productos
                           SET stock = ?
                           WHERE id = ?""",
                           (stock_actualizado, id_producto)
                           )
            modificado = True
    if modificado:
        conexion.commit()
        producto = obtener_producto_por_id(conexion, id_producto)
        return producto
    return None