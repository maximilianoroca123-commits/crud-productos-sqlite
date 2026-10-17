def paginar_productos(
    productos_filtrados, 
    pagina: int = 1,
    limite: int = 10):
        inicio = (pagina - 1) * limite
        fin = inicio + limite
        productos_pagina = productos_filtrados[inicio:fin]
        return productos_pagina
def calcular_cantidad_paginas(total: int, limite: int):
    cantidad_de_paginas = total // limite
    productos_sobrantes = total % limite
    if productos_sobrantes != 0:
        cantidad_de_paginas += 1
    return cantidad_de_paginas