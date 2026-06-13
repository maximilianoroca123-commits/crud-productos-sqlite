def mostrar_resultados(resultados):
    if not resultados:
        print("No hay resultados")
        return

    for resultado in resultados:
        print(f"ID: {resultado[0]}")
        print(f"Nombre: {resultado[1]}")
        print(f"Categoria: {resultado[2]}")
        print(f"Precio: {resultado[3]}")
        print(f"Stock: {resultado[4]}")
        print("----------------")

def pausar():
    input("Presione ENTER para continuar...")