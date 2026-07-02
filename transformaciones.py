from config import CAMPOS_POSIBLES

def obtener_valor_campo(producto_api, campos_posibles):
    for campo in campos_posibles:
        if campo in producto_api:
            return producto_api[campo]
    return None

def transformar_producto(producto_api):
    nombre = obtener_valor_campo(producto_api, CAMPOS_POSIBLES["nombre"])
    categoria = obtener_valor_campo(producto_api, CAMPOS_POSIBLES["categoria"])
    precio = obtener_valor_campo(producto_api, CAMPOS_POSIBLES["precio"])
    stock = obtener_valor_campo(producto_api, CAMPOS_POSIBLES["stock"])
    if stock is None:
        stock = 0
    if nombre is None or categoria is None or precio is None:
        return None
    producto = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
        }
    return producto

def transformar_productos(productos_api):
    productos_normalizados = []
    recibidos = 0
    normalizados = 0
    invalidos = 0
    for producto in productos_api:
        recibidos += 1
        resultado = transformar_producto(producto)
        if resultado is not None:
            normalizados += 1
            productos_normalizados.append(resultado)
        else:
            invalidos += 1
    return {
    "productos_normalizados": productos_normalizados,
    "recibidos": recibidos,
    "normalizados": normalizados,
    "invalidos": invalidos
}