import requests

datos_producto = {
    "stock": 3
}
#respuesta = requests.post(
#"http://127.0.0.1:8000/productos",
#json=datos_producto
#)

respuesta = requests.get(
"http://127.0.0.1:8000/productos?categoria=tecnologia&precio_min=1000&precio_max=8500&pagina=1&limite=11"
)

#respuesta = requests.delete(
#"http://127.0.0.1:8000/productos/8"
#)

#respuesta = requests.patch(
#   "http://127.0.0.1:8000/productos/8",
#   json=datos_producto
#)
print(respuesta.status_code)
print(respuesta.json())