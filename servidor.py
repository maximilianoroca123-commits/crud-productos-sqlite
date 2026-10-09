from typing import Annotated, Literal
from busqueda import obtener_producto_por_id
from fastapi import FastAPI, HTTPException
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
)

from config import CATEGORIAS_VALIDAS


# Aplicación FastAPI

app = FastAPI()


# Datos en memoria

productos = [
    {
        "id": 1,
        "nombre": "Mouse",
        "categoria": "tecnologia",
        "precio": 8500,
        "stock": 5,
    },
    {
        "id": 2,
        "nombre": "teclado",
        "categoria": "tecnologia",
        "precio": 7500,
        "stock": 5,
    },
]


# Funciones auxiliares

def generar_id(productos):
    mayor_id = 0

    for existente in productos:
        if mayor_id < existente["id"]:
            mayor_id = existente["id"]

    mayor_id += 1
    return mayor_id


def normalizar_categoria(valor):
    if isinstance(valor, str):
        return valor.strip().lower()

    return valor

# Modelos de entrada

class ProductoCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
    ]

    categoria: Annotated[
        Literal["alimento", "tecnologia", "libreria"],
        BeforeValidator(normalizar_categoria),
    ]

    precio: int = Field(gt=0, strict=True)
    stock: int = Field(default=0, ge=0, strict=True)


class ProductoActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    precio: int = Field(default=1, gt=0, strict=True)
    stock: int = Field(default=0, ge=0, strict=True)


# GET: listar, filtrar y paginar productos

@app.get("/productos")
def listar_productos(
    categoria: str | None = None,
    precio_min: int | None = None,
    precio_max: int | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    # Validaciones de entrada

    if pagina <= 0 or limite <= 0:
        raise HTTPException(
            status_code=422,
            detail="pagina y limite deben ser mayores que 0",
        )

    if categoria is not None and categoria not in CATEGORIAS_VALIDAS:
        raise HTTPException(
            status_code=422,
            detail="categoria invalida",
        )

    if precio_min is not None and precio_min < 0:
        raise HTTPException(
            status_code=422,
            detail="precio minimo debe ser igual o mayor a 0",
        )

    if precio_max is not None and precio_max < 0:
        raise HTTPException(
            status_code=422,
            detail="precio maximo debe ser igual o mayor a 0",
        )

    if (
        precio_min is not None
        and precio_max is not None
        and precio_min > precio_max
    ):
        raise HTTPException(
            status_code=422,
            detail="precio_min no puede ser mayor que precio_max",
        )

    # Filtrado

    productos_filtrados = []

    for producto in productos:
        if (
            (categoria is None or producto["categoria"] == categoria)
            and (precio_min is None or producto["precio"] >= precio_min)
            and (precio_max is None or producto["precio"] <= precio_max)
        ):
            productos_filtrados.append(producto)

    # Paginación

    inicio = (pagina - 1) * limite
    fin = inicio + limite
    productos_pagina = productos_filtrados[inicio:fin]

    # Metadatos

    total = len(productos_filtrados)
    cantidad_de_paginas = total // limite
    productos_sobrantes = total % limite

    if productos_sobrantes != 0:
        cantidad_de_paginas += 1

    return {
        "productos": productos_pagina,
        "total": total,
        "cantidad_paginas": cantidad_de_paginas,
        "pagina": pagina,
        "limite": limite,
    }


# GET: consultar un producto por ID

@app.get("/productos/{id}")
def consultar_producto(id: int):
    producto_existente = obtener_producto_por_id(id, productos)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    return producto_existente

# POST: crear un producto

@app.post("/productos", status_code=201)
def recibir_producto(producto: ProductoCrear):
    # Comprobación de duplicados

    for existente in productos:
        if existente["nombre"].lower() == producto.nombre.lower():
            raise HTTPException(
                status_code=409,
                detail="El producto ya existe",
            )

    # Construcción del producto

    nuevo_id = generar_id(productos)

    nuevo_producto = {
        "id": nuevo_id,
        "nombre": producto.nombre,
        "categoria": producto.categoria,
        "precio": producto.precio,
        "stock": producto.stock,
    }

    # Incorporación a la lista

    productos.append(nuevo_producto)
    return nuevo_producto


# PATCH: actualizar precio y/o stock

@app.patch("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoActualizar):
    # Obtención de los campos enviados

    cambios = producto.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            status_code=422,
            detail="No se enviaron campos a actualizar",
        )

    # Búsqueda y actualización

    producto_existente = obtener_producto_por_id(id, productos)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )

    if "stock" in cambios:
        producto_existente["stock"] = cambios["stock"]

    if "precio" in cambios:
        producto_existente["precio"] = cambios["precio"]

    return producto_existente


# DELETE: eliminar un producto

@app.delete("/productos/{id}", status_code=204)
def eliminar_producto(id: int):
    producto_existente = obtener_producto_por_id(id, productos)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    productos.remove(producto_existente)
