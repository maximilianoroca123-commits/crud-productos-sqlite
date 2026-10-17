productos = [
    {
        "id": 1,
        "nombre": "Mouse",
        "categoria": "tecnologia",
        "precio": 8500,
        "stock": 5,
    },
    {
        "id": 2,
        "nombre": "teclado",
        "categoria": "tecnologia",
        "precio": 7500,
        "stock": 5,
    },
]
def obtener_todos_los_productos():
    return productos
def obtener_producto_por_id(id: int):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return None

def obtener_producto_por_nombre(nombre: str):
    for existente in productos:
        if existente["nombre"].lower() == nombre.lower():
            return existente
    return None

def agregar_producto(producto):
    productos.append(producto)

def quitar_producto(producto):
    productos.remove(producto)    

def guardar_producto_actualizado(producto_actualizado):
    for posicion, producto in enumerate(productos):
        if producto["id"] == producto_actualizado["id"]:
            productos[posicion] = producto_actualizado
            return