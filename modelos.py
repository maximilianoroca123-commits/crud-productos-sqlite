from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
)
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