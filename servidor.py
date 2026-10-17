# Rutas HTTP, coordinación de operaciones y respuestas de la API.

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from config import CATEGORIAS_VALIDAS
from errores import ProductoDuplicadoError, ProductoNoEncontradoError, ErrorPersistencia
from logica_productos import aplicar_cambios_producto
from modelos import ProductoCrear, ProductoActualizar
from paginacion import calcular_cantidad_paginas
from repositorio_sqlite import (
    obtener_producto_por_id,
    obtener_producto_por_nombre,
    crear_producto,
    guardar_producto_actualizado,
    eliminar_producto as eliminar_producto_sqlite,
    contar_productos,
    obtener_productos_paginados,
)

logger = logging.getLogger("uvicorn.error")

app = FastAPI()


@app.exception_handler(ErrorPersistencia)
async def manejar_error_persistencia(
    request: Request,
    error: ErrorPersistencia,
):
    # El cliente recibe un mensaje genérico; el log conserva la causa.
    logger.error(
        "Fallo de persistencia en %s %s",
        request.method,
        request.url.path,
        exc_info=(type(error), error, error.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "No se pudo completar la operación"},
    )


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

    if pagina < 1:
        raise HTTPException(
            status_code=422,
            detail="pagina debe ser mayor o igual a 1",
        )

    if not 1 <= limite <= 10:
        raise HTTPException(
            status_code=422,
            detail="limite debe estar entre 1 y 10",
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

    if precio_min is not None and precio_max is not None and precio_min > precio_max:
        raise HTTPException(
            status_code=422,
            detail="precio_min no puede ser mayor que precio_max",
        )

    # Consulta solo la página pedida; el total se obtiene por separado.
    productos_pagina = obtener_productos_paginados(
        pagina, limite, categoria, precio_min, precio_max
    )

    # Metadatos

    total = contar_productos(categoria, precio_min, precio_max)
    cantidad_de_paginas = calcular_cantidad_paginas(total, limite)
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
    producto_existente = obtener_producto_por_id(id)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    return producto_existente


# POST: crear un producto


@app.post("/productos", status_code=201)
def recibir_producto(producto: ProductoCrear):
    producto_existente = obtener_producto_por_nombre(producto.nombre)
    if producto_existente is not None:
        raise HTTPException(
            status_code=409,
            detail="El producto ya existe",
        )
    # El índice único también protege si hay solicitudes concurrentes.
    try:
        nuevo_producto = crear_producto(
            producto.nombre,
            producto.categoria,
            producto.precio,
            producto.stock,
        )
        return nuevo_producto
    except ProductoDuplicadoError:
        raise HTTPException(
            status_code=409,
            detail="El producto ya existe",
        )


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

    producto_existente = obtener_producto_por_id(id)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    producto_actualizado = aplicar_cambios_producto(producto_existente, cambios)
    try:
        guardar_producto_actualizado(producto_actualizado)
    except ProductoNoEncontradoError:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    return producto_actualizado


# DELETE: eliminar un producto


@app.delete("/productos/{id}", status_code=204)
def eliminar_producto(id: int):
    producto_existente = obtener_producto_por_id(id)
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    try:
        eliminar_producto_sqlite(id)
    except ProductoNoEncontradoError:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
