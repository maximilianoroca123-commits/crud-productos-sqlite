from api import obtener_productos_api
from transformaciones import transformar_productos
from filtros import filtrar_productos_nuevos
from persistencia import guardar_productos

def importar_productos_api(conexion):
    productos_api = obtener_productos_api()
    resultado_transformacion = transformar_productos(productos_api)
    resultado_filtrado = filtrar_productos_nuevos(conexion, resultado_transformacion["productos_normalizados"])
    cantidad_guardada = guardar_productos(conexion, resultado_filtrado["productos_nuevos"])
    
    print(f"Productos recibidos: {resultado_transformacion['recibidos']}")
    print(f"Productos normalizados: {resultado_transformacion['normalizados']}")
    print(f"Productos invalidos: {resultado_transformacion['invalidos']}")
    print(f"Productos nuevos: {resultado_filtrado['nuevos']}")
    print(f"Productos duplicados: {resultado_filtrado['duplicados']}")
    print(f"Productos guardados: {cantidad_guardada}")