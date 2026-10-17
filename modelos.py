# Contrato de los cuerpos JSON recibidos por la API.

from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
)


# Normaliza texto y deja los demás tipos para que los valide el modelo.
def normalizar_categoria(valor):
    if isinstance(valor, str):
        return valor.strip().lower()

    return valor


# Modelos de entrada


# Valida los campos de creación y rechaza los campos adicionales.
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


# Permite omitir campos; la ruta exige al menos un cambio.
class ProductoActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # exclude_unset=True evita que los valores por defecto se apliquen al PATCH.
    precio: int = Field(default=1, gt=0, strict=True)
    stock: int = Field(default=0, ge=0, strict=True)
