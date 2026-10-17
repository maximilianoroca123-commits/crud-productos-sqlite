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

def filtrar_productos(productos,
        categoria: str | None = None,
        precio_min: int | None = None,
        precio_max: int | None = None):
    productos_filtrados = []

    for producto in productos:
        if (
            (categoria is None or producto["categoria"] == categoria)
            and (precio_min is None or producto["precio"] >= precio_min)
            and (precio_max is None or producto["precio"] <= precio_max)
        ):
            productos_filtrados.append(producto)
    return productos_filtrados