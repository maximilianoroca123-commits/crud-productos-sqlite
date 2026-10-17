# Excepciones del programa, independientes de HTTP y SQLite.


# Indica un conflicto con un nombre ya registrado.
class ProductoDuplicadoError(Exception):
    pass


# Indica que la operación no encontró la fila esperada.
class ProductoNoEncontradoError(Exception):
    pass


# Representa un fallo interno al acceder o escribir en la base.
class ErrorPersistencia(Exception):
    pass
