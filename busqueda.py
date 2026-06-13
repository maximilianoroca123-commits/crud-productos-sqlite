from validaciones import pedir_opcion, pedir_numero
from config import CATEGORIAS_VALIDAS

def crear_filtros():
    operadores_validos = ["==", ">", "<", ">=", "<="]
    claves_texto_libre = ["nombre"]
    claves_opciones = ["categoria"]
    claves_directas = claves_texto_libre + claves_opciones
    claves_con_operador = ["precio", "stock"]
    claves_validas = claves_directas + claves_con_operador

    consulta = pedir_opcion("Desea continuar?: ", ["si", "no"])
    filtros = {}

    while consulta == "si":
        clave = pedir_opcion("Ingrese una clave: ", claves_validas)

        if clave in claves_texto_libre:
            valor = input("Ingrese valor: ").lower().strip()
            filtros[clave] = valor

        elif clave in claves_opciones:
            valor = pedir_opcion("Ingrese categoría: ", CATEGORIAS_VALIDAS)
            filtros[clave] = valor

        elif clave in claves_con_operador:
            operador = pedir_opcion("Ingrese operador: ", operadores_validos)
            valor = pedir_numero("Ingrese valor: ")
            filtros[clave] = (operador, valor)

        consulta = pedir_opcion("Desea continuar?: ", ["si", "no"])

    return filtros



def buscar(conexion, filtros):
    if not filtros:
        return []
    condiciones = []
    valores = []

    for clave, condicion in filtros.items():
        if isinstance(condicion, tuple):
            operador, valor = condicion
            condiciones.append(f"{clave} {operador} ?")
            valores.append(valor)
        else:
            condiciones.append(f"{clave} = ?")
            valores.append(condicion)
    where = " AND ".join(condiciones)
    cursor = conexion.cursor()
    sql = f"SELECT * FROM productos WHERE {where}"
    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    return resultado

def obtener_producto_por_nombre(conexion, nombre):

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM productos WHERE nombre = ?",
        (nombre,)
    )

    resultado = cursor.fetchone()

    return resultado

def obtener_todos_los_productos(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT * FROM productos""")
    resultado = cursor.fetchall()
    return resultado

def obtener_producto_por_id(conexion, id_producto):
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM productos WHERE id = ?",
        (id_producto,)
    )
    resultado = cursor.fetchone()
    return resultado