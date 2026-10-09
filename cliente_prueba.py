import requests

datos_producto = {
    "stock": 0
}
#respuesta = requests.post(
 # "http://127.0.0.1:8000/productos",
 #   json=datos_producto
#)

respuesta = requests.get(
  "http://127.0.0.1:8000/productos/3"
)
#respuesta = requests.delete(
#"http://127.0.0.1:8000/productos/2"
#)

#respuesta = requests.patch(
#    "http://127.0.0.1:8000/productos/3",
#    json=datos_producto
#)
print(respuesta.status_code)
print(respuesta.json())