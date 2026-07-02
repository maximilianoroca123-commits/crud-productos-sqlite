from persistencia import obtener_producto_por_nombre

def filtrar_productos_nuevos(conexion, productos):
    productos_nuevos = []
    nuevos = 0
    duplicados = 0
    for producto in productos:
        producto_existente = obtener_producto_por_nombre(conexion, producto["nombre"])
        if producto_existente is None:
            nuevos += 1
            productos_nuevos.append(producto)
        else:
            duplicados += 1
    return {
    "productos_nuevos": productos_nuevos,
    "nuevos": nuevos,
    "duplicados": duplicados
}