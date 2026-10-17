# Configuración compartida por la API y el CRUD de consola.

from pathlib import Path

# La API localiza su base respecto de este archivo.
CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_DB_API = CARPETA_PROYECTO / "productos_api.db"
# El programa de consola conserva sus rutas anteriores.
RUTA_DB = "productos.db"
RUTA_LOGS = "logs.txt"
CATEGORIAS_VALIDAS = ["alimento", "tecnologia", "libreria"]
# Configuración de la importación externa.
URL_API = "https://fakestoreapi.com/products"
CAMPOS_POSIBLES = {
    "nombre": ["title", "name", "nombre_producto"],
    "categoria": ["category", "categoria", "tipo"],
    "precio": ["price", "precio", "cost"],
    "stock": ["stock", "cantidad", "quantity"],
}
