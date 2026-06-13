from validaciones import pedir_opcion
from presentacion import pausar, mostrar_resultados
from busqueda import crear_filtros, buscar, obtener_todos_los_productos
from persistencia import registrar_log
from crud import registrar_producto, eliminar_producto, actualizar_producto

def menu(conexion):
    while True:
        print("1. Buscar productos")
        print("2. Mostrar todos los productos")
        print("3. Crear producto")
        print("4. Eliminar producto")
        print("5. Actualizar producto")
        print("6. Salir")

        opcion = pedir_opcion(
            "Ingrese una opcion: ",
            ["1", "2", "3", "4", "5", "6"]
        )

        if opcion == "1":
            filtros = crear_filtros()
            resultados = buscar(conexion, filtros)
            mostrar_resultados(resultados)
            pausar()

        elif opcion == "2":
            resultados = obtener_todos_los_productos(conexion)
            mostrar_resultados(resultados)
            pausar()

        elif opcion == "3":
            resultado = registrar_producto(conexion)

            if resultado:
                registrar_log(f"Producto creado: ID {resultado['id']} - {resultado['nombre']}")
                print(f"Producto creado: ID {resultado['id']} - {resultado['nombre']}")
            else:
                print("El producto ya existe")
            pausar()

        elif opcion == "4":
            resultado = eliminar_producto(conexion)

            if resultado:
                registrar_log(f"Producto eliminado: ID {resultado[0]} - {resultado[1]}")
                print(f"Producto eliminado: ID {resultado[0]} - {resultado[1]}")
            else:
                print("Producto no encontrado")

            pausar()

        elif opcion == "5":
            resultado = actualizar_producto(conexion)

            if resultado:
                registrar_log(f"Producto actualizado: ID {resultado[0]} - {resultado[1]}")
                print(f"Producto actualizado: ID {resultado[0]} - {resultado[1]}")
            else:
                print("Se canceló la actualización o no se encontró el producto")

            pausar()

        elif opcion == "6":
            print("Programa finalizado")
            break