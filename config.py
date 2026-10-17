from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_DB_API = CARPETA_PROYECTO / "productos_api.db"
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