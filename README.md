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
Los productos obtenidos desde la API se normalizan al formato interno del sistema, se validan, se filtran duplicados y finalmente se almacenan en SQLite.

## Arquitectura

config.py
Configuración del sistema.

api.py
Comunicación con APIs externas.

transformaciones.py
Normalización de datos.

filtros.py
Filtrado de productos.

persistencia.py
Acceso a SQLite.

importador.py
Coordinación del proceso de importación.

main.py
Punto de entrada del programa.