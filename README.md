# API de productos con FastAPI y SQLite

Proyecto de aprendizaje backend desarrollado en Python. Permite crear, consultar, filtrar, actualizar y eliminar productos mediante una API HTTP con persistencia en SQLite.

El repositorio conserva la etapa anterior: un CRUD de consola con importación de productos desde una API externa. Ambas aplicaciones tienen puntos de entrada y bases de datos diferentes.

## Funcionalidades de la API

- Creación de productos con ID generado por SQLite.
- Consulta individual por ID.
- Listado con filtros combinables por categoría y rango de precios.
- Paginación en SQL con orden por ID ascendente y metadatos.
- Actualización parcial de precio y stock.
- Eliminación de productos.
- Validación de cuerpos JSON con Pydantic y rechazo de campos adicionales.
- Detección de nombres duplicados y protección mediante un índice único.
- Restricciones de base de datos para precios positivos y stock no negativo, sin valores nulos.
- Traducción de excepciones del repositorio a respuestas HTTP.
- Registro de errores de persistencia en la terminal del servidor.

## Tecnologías

Python, FastAPI, Pydantic, Uvicorn, SQLite y Requests.

Las versiones de las dependencias directas están en `requirements.txt`. `sqlite3`, `logging`, `pathlib`, `datetime` y `typing` forman parte de la biblioteca estándar de Python.

## Instalación e inicio

Ejecutar los comandos desde la carpeta que contiene `servidor.py`.

### 1. Requisitos

- Python: el proyecto se desarrolló con Python 3.14. La revisión de esta entrega también se ejecutó con Python 3.12.
- Acceso a una terminal.
- Git, si se descarga el proyecto mediante clonación.

Para descargarlo con Git:

```powershell
git clone https://github.com/maximilianoroca123-commits/crud-productos-sqlite.git
cd crud-productos-sqlite
```

También se puede descargar y extraer el proyecto como ZIP y abrir una terminal en su carpeta.

### 2. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

El archivo fija las dependencias directas; sus dependencias transitivas se resuelven durante la instalación.

### 3. Preparar la base de la API

```powershell
python preparar_db_api.py
```

El script crea `productos_api.db` junto a `config.py`, define la tabla y el índice único, y carga tres productos de ejemplo si la tabla está vacía: Mouse, teclado y Pan.

Si la tabla ya contiene productos, no vuelve a cargar esos ejemplos. Es normal que el script termine sin imprimir mensajes. No modifica `productos.db`, que pertenece al CRUD de consola.

`CREATE TABLE IF NOT EXISTS` no actualiza el esquema de una tabla existente. Para una base antigua de la API sin las restricciones de precio y stock, consultar la sección de migración.

### 4. Iniciar el servidor

```powershell
python -m uvicorn servidor:app
```

El servidor queda disponible en `http://127.0.0.1:8000`. Para detenerlo, presionar **Ctrl+C**. Sin recarga automática, los cambios guardados en el código requieren reiniciar el servidor.

Los productos se guardan en SQLite: reiniciar Uvicorn no restablece los datos iniciales.

### 5. Consultar la API

Abrir en el navegador:

```text
http://127.0.0.1:8000/productos
```

La documentación interactiva está disponible en:

```text
http://127.0.0.1:8000/docs
```

Las condiciones comprobadas manualmente dentro de las rutas, como la relación entre los precios mínimo y máximo, están descritas en este README; no todas aparecen como restricciones del esquema generado.

## Rutas

| Método | Ruta | Operación | Respuesta de éxito |
| --- | --- | --- | --- |
| GET | `/productos` | Listar, filtrar y paginar | 200 con productos y metadatos |
| GET | `/productos/{id}` | Consultar un producto | 200 con el producto |
| POST | `/productos` | Crear un producto | 201 con el producto creado |
| PATCH | `/productos/{id}` | Modificar precio y/o stock | 200 con el producto actualizado |
| DELETE | `/productos/{id}` | Eliminar un producto | 204 sin cuerpo |

No se ofrece PUT. El ID de la ruta debe poder interpretarse como un entero.

## Contrato de entrada

### Crear un producto

Ejemplo de cuerpo para `POST /productos`:

```json
{
  "nombre": "Microfono",
  "categoria": "tecnologia",
  "precio": 1200,
  "stock": 0
}
```

| Campo | Regla |
| --- | --- |
| `nombre` | Texto obligatorio. Se quitan espacios de los extremos y debe quedar al menos un carácter. |
| `categoria` | Texto obligatorio: `alimento`, `tecnologia` o `libreria`. Se quitan espacios de los extremos y se convierte a minúsculas. |
| `precio` | Entero obligatorio mayor que 0. |
| `stock` | Entero mayor o igual que 0. Si se omite, se usa 0. |

Precio y stock rechazan cadenas numéricas, decimales, booleanos y `null`. El cliente no debe enviar `id`: lo genera SQLite. Se rechazan campos adicionales.

Los nombres duplicados se comparan sin distinguir mayúsculas y minúsculas para caracteres ASCII. Por ejemplo, `Mouse` y `mOuSe` se consideran el mismo nombre. Ver la limitación sobre Unicode más abajo.

### Actualizar un producto

Ejemplo de cuerpo para `PATCH /productos/1`:

```json
{
  "stock": 3
}
```

Solo se aceptan `precio` y `stock`, con las mismas reglas numéricas de creación. Debe enviarse al menos uno. Los campos omitidos conservan sus valores actuales; enviar stock 0 sí lo actualiza a 0.

Se rechazan el cuerpo vacío `{}`, `null` en los campos y cualquier campo adicional. Nombre, categoría e ID no se modifican mediante PATCH.

### Listar productos

Ejemplo:

```text
GET /productos?categoria=tecnologia&precio_min=1000&precio_max=8500&pagina=1&limite=1
```

| Parámetro | Regla | Valor por defecto |
| --- | --- | --- |
| `categoria` | Una de las categorías permitidas, escrita exactamente en minúsculas | Sin filtro |
| `precio_min` | Entero mayor o igual que 0; límite inclusivo | Sin filtro |
| `precio_max` | Entero mayor o igual que 0; límite inclusivo | Sin filtro |
| `pagina` | Entero mayor o igual que 1 | 1 |
| `limite` | Entero entre 1 y 10, inclusive | 10 |

Si se envían ambos precios, `precio_min` no puede superar a `precio_max`. Los filtros se combinan con AND. La categoría del query no se normaliza como la del cuerpo de creación.

El listado devuelve un objeto con esta estructura:

```json
{
  "productos": [
    {
      "id": 1,
      "nombre": "Mouse",
      "categoria": "tecnologia",
      "precio": 8500,
      "stock": 7
    }
  ],
  "total": 2,
  "cantidad_paginas": 2,
  "pagina": 1,
  "limite": 1
}
```

Ejemplo ilustrativo: los valores dependen de los datos actuales de la base.

`total` cuenta todos los productos que cumplen los filtros antes de paginar. Una página posterior a la última devuelve 200 con `productos: []` y conserva los metadatos del conjunto filtrado. Si no hay ninguna coincidencia, `total` y `cantidad_paginas` son 0.

## Respuestas de error

| Código | Casos principales |
| --- | --- |
| 404 | El producto solicitado no existe, o desapareció antes de actualizarlo o eliminarlo. |
| 405 | El método HTTP no está registrado para esa ruta. |
| 409 | El nombre del producto ya existe. |
| 422 | El cuerpo, un parámetro de ruta o un query incumple el contrato. |
| 500 | Una operación del repositorio falla y se traduce a `ErrorPersistencia`. |

Para errores de persistencia manejados, el cliente recibe:

```json
{
  "detail": "No se pudo completar la operación"
}
```

Los detalles y la causa original quedan en el log de la terminal del servidor. La API no configura actualmente un archivo de logs; `logs.txt` corresponde al programa de consola anterior.

## Organización del código

El recorrido principal es: la ruta recibe y valida la solicitud, coordina la lógica necesaria y llama al repositorio; este ejecuta SQL y convierte las filas en diccionarios. La ruta devuelve los datos o traduce las excepciones a respuestas HTTP.

| Archivo | Responsabilidad |
| --- | --- |
| `servidor.py` | Aplicación FastAPI, rutas y manejador de errores de persistencia. |
| `modelos.py` | Modelos Pydantic para crear y actualizar productos. |
| `logica_productos.py` | Construcción de productos y aplicación de cambios sobre una copia. |
| `repositorio_sqlite.py` | Conexiones, consultas, escrituras, paginación y traducción de errores SQLite. |
| `errores.py` | Excepciones propias, sin dependencia de HTTP. |
| `paginacion.py` | Cálculo de la cantidad de páginas. |
| `config.py` | Rutas y constantes compartidas. |
| `preparar_db_api.py` | Preparación de una base nueva y carga de ejemplos. |
| `migrar_checks_productos.py` | Migración del esquema anterior de la API. |
| `cliente_prueba.py` | Solicitudes HTTP manuales con Requests. |
| `prueba_repositorio.py` | Consultas y ejemplos manuales del repositorio sin HTTP. |
| `requirements.txt` | Dependencias directas con versiones fijadas. |

El repositorio no genera respuestas HTTP: distingue duplicados, productos ausentes y fallos de persistencia mediante excepciones propias. La base conserva la protección final frente a duplicados, incluso si dos solicitudes superan la búsqueda previa.

## Pruebas manuales

Con Uvicorn en ejecución, abrir otra terminal en la carpeta del proyecto:

```powershell
python cliente_prueba.py
```

El archivo conserva ejemplos de GET, POST, PATCH y DELETE para activar de uno en uno. La consulta actualmente activa usa `limite=11` deliberadamente y espera 422.

Para una respuesta 204, usar `respuesta.text` en lugar de `respuesta.json()`: no hay un cuerpo JSON para interpretar. Los IDs usados en ejemplos deben ajustarse a la base actual.

Para probar el repositorio directamente:

```powershell
python prueba_repositorio.py
```

Los ejemplos están comentados; se debe activar únicamente la prueba que se quiera ejecutar. Algunos ejemplos intentan escrituras inválidas para comprobar las restricciones y producen excepciones esperadas.

Durante el desarrollo se comprobaron creación, consulta, actualización parcial, persistencia tras reiniciar, eliminación, duplicados, validaciones, filtros, paginación, metadatos, errores internos y restricciones SQL.

Estos archivos son herramientas de prueba manual. El repositorio todavía no contiene una suite automatizada permanente.

## Migración de una base anterior

`migrar_checks_productos.py` se preparó para la tabla anterior de la API, con los mismos cinco campos, antes de incorporar CHECK y NOT NULL a precio y stock. Una base nueva creada con `preparar_db_api.py` ya tiene esas restricciones y no necesita este paso.

Con el servidor detenido, guardar un respaldo de la base anterior. En PowerShell, si todavía no existe ese respaldo:

```powershell
Copy-Item ".\productos_api.db" ".\productos_api_antes_checks.db"
```

Después:

```powershell
python migrar_checks_productos.py
```

La migración copia los datos a una tabla nueva, comprueba cantidad y contenido, reemplaza la tabla, conserva el historial de IDs y recrea el índice único. Todo se ejecuta dentro de una transacción: si falla, se aplica rollback.

Es una migración puntual para este esquema, no un sistema general de migraciones. No ejecutar sobre `productos.db`, la base de consola. La copia a la tabla nueva puede fallar si los datos existentes incumplen las restricciones; los nombres duplicados también impiden crear el índice único.

## Etapa anterior: CRUD de consola e importador

Para iniciar el programa anterior:

```powershell
python main.py
```

Ejecutarlo desde la carpeta del proyecto: esta etapa conserva las rutas relativas `productos.db` y `logs.txt`.

El menú permite buscar, listar, crear, actualizar y eliminar productos e importar desde la API externa. La importación requiere acceso a Internet y que el servicio externo esté disponible.

| Archivo | Responsabilidad en la etapa de consola |
| --- | --- |
| `main.py` | Inicio de la aplicación. |
| `menu.py` | Menú y coordinación de acciones. |
| `crud.py` | Operaciones interactivas sobre productos. |
| `busqueda.py` | Construcción de filtros y consultas SQL. |
| `validaciones.py` | Lectura de opciones y números desde la terminal. |
| `presentacion.py` | Impresión de resultados y pausas. |
| `persistencia.py` | Acceso a la base de consola, guardado por lote y logs. |
| `api.py` | Consulta de la API externa. |
| `transformaciones.py` | Adaptación de campos externos. |
| `filtros.py` | Exclusión de nombres ya guardados antes de importar. |
| `importador.py` | Coordinación de la importación y su resumen. |

La API HTTP trabaja con una base separada porque el contrato actual es más estricto que los datos importados durante esta etapa anterior. La preparación de la API reutiliza `guardar_productos` de `persistencia.py` pasando su propia conexión.

## Alcance y limitaciones actuales

Esta versión es un proyecto educativo ejecutado localmente.

- No incluye autenticación, autorización ni configuración de despliegue público.
- El índice usa `LOWER(nombre)` de SQLite, que por defecto convierte a minúsculas los caracteres ASCII. La comparación completa de nombres con Unicode queda pendiente.
- Pydantic exige enteros estrictos en precio y stock. La base verifica rangos y ausencia de NULL, pero declarar una columna INTEGER no impone por sí solo esa misma validación estricta; tampoco se trasladaron aún todas las reglas de nombre y categoría a SQL.
- PATCH consulta el producto y después guarda precio y stock. No incorpora control de versiones para evitar la pérdida de cambios entre actualizaciones concurrentes.
- La página y el total se consultan en conexiones separadas. Si hay escrituras concurrentes entre ambas consultas, podrían reflejar momentos distintos de la base.

Las bases locales, respaldos y logs no se versionan. La base de la API se puede preparar con el script incluido; los datos históricos de consola no se distribuyen en esta entrega de código.
