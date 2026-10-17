# Construcción y actualización de diccionarios de productos.


# Reúne el ID y los campos en el formato usado por la API.
def construir_producto(id, nombre, categoria, precio, stock):
    nuevo_producto = {
        "id": id,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
    }
    return nuevo_producto


# Copia el producto antes de aplicar los campos enviados.
def aplicar_cambios_producto(producto, cambios):
    producto_actualizado = producto.copy()
    if "stock" in cambios:
        producto_actualizado["stock"] = cambios["stock"]
    if "precio" in cambios:
        producto_actualizado["precio"] = cambios["precio"]
    return producto_actualizado
