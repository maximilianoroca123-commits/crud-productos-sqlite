# Cálculo de metadatos a partir del total filtrado.


# Incluye una página adicional cuando hay productos sobrantes.
def calcular_cantidad_paginas(total: int, limite: int):
    cantidad_de_paginas = total // limite
    productos_sobrantes = total % limite
    if productos_sobrantes != 0:
        cantidad_de_paginas += 1
    return cantidad_de_paginas
