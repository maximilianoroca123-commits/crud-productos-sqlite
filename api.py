import requests
from config import URL_API

def obtener_productos_api():
    respuesta = requests.get(URL_API)
    return respuesta.json()