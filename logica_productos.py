def generar_id(productos):
    mayor_id = 0

    for existente in productos:
        if mayor_id < existente["id"]:
            mayor_id = existente["id"]

    mayor_id += 1
    return mayor_id

def construir_producto(id, nombre, categoria, precio, stock):
    nuevo_producto = {
        "id": id,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
    }
    return nuevo_producto

def aplicar_cambios_producto(producto, cambios):
    producto_actualizado = producto.copy()
    if "stock" in cambios:
        producto_actualizado["stock"] = cambios["stock"]
    if "precio" in cambios:
        producto_actualizado["precio"] = cambios["precio"]
    return producto_actualizado