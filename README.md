# CRUD de Productos con SQLite

Proyecto realizado en Python.

## Características

- Crear productos
- Buscar productos con filtros dinámicos
- Actualizar productos
- Eliminar productos
- Persistencia con SQLite
- Registro de logs
- Importar productos desde API externa
- Normalización de datos recibidos
- Filtrado de duplicados antes de guardar
- Resumen de importación
## Tecnologías

- Python
- SQLite
- requests
- API externa / JSON

## Importación desde API

El sistema permite importar productos desde una API externa.  
Los datos recibidos se transforman al formato interno del programa, se filtran duplicados y luego se guardan en SQLite.