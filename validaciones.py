def solicitar_id():
    id_producto = pedir_numero("Ingrese ID de producto: ")
    return id_producto

def solicitar_nombre():
     nombre = input("Ingrese el nombre del producto: ").lower().strip()
     return nombre

def pedir_opcion(mensaje, opciones_validas):
    opcion_de_usuario = input(mensaje).lower().strip()

    while opcion_de_usuario not in opciones_validas:
        print("Opcion invalida")
        opcion_de_usuario = input("Ingrese una opcion valida: ").lower().strip()

    return opcion_de_usuario

def pedir_numero(mensaje):
    while True:
        try:
            num = int(input(mensaje))
            break
        except ValueError:
            print("Entrada invalida, ingrese un numero por favor")

    return num