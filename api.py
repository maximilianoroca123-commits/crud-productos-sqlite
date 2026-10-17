# Consulta de la API externa para el importador de consola.

import requests

from config import URL_API


# Obtiene el cuerpo JSON devuelto por la API externa.
def obtener_productos_api():
    respuesta = requests.get(URL_API)
    return respuesta.json()
