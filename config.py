RUTA_DB = "productos.db"
RUTA_LOGS = "logs.txt"
CATEGORIAS_VALIDAS = ["alimento", "tecnologia", "libreria"]
URL_API = "https://fakestoreapi.com/products"
CAMPOS_POSIBLES = {
    "nombre": [
        "title",
        "name",
        "nombre_producto"
    ],

    "categoria": [
        "category",
        "categoria",
        "tipo"
    ],

    "precio": [
        "price",
        "precio",
        "cost"
    ],

    "stock": [
        "stock",
        "cantidad",
        "quantity"
    ]
}