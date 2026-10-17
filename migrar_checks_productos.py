from repositorio_sqlite import conectar_db

def migrar_checks_productos():
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("BEGIN")
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = ?",
                       ("productos",),)
        fila_secuencia = cursor.fetchone()
        if fila_secuencia is None:
            secuencia_original = 0
        else:
            secuencia_original = fila_secuencia[0]
        cursor.execute("""CREATE TABLE productos_nueva (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        categoria TEXT,
                        precio INTEGER NOT NULL CHECK (precio > 0),
                        stock INTEGER NOT NULL CHECK (stock >= 0)
                    )
                    """)
        cursor.execute("""INSERT INTO productos_nueva 
                        (id, nombre, categoria, precio, stock)
                        SELECT id, nombre, categoria, precio, stock
                        FROM productos""")
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_original = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM productos_nueva")
        total_nuevo = cursor.fetchone()[0]
        if total_original != total_nuevo:
            raise RuntimeError("La cantidad de productos copiados no coincide")
        cursor.execute("""SELECT id, nombre, categoria, precio, stock FROM productos
                       EXCEPT
                       SELECT id, nombre, categoria, precio, stock FROM productos_nueva""")
        diferencias = cursor.fetchall()
        if diferencias:
            raise RuntimeError("Los datos copiados no coinciden con los originales")
        cursor.execute("DROP TABLE productos")
        cursor.execute("ALTER TABLE productos_nueva RENAME TO productos")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?",
                       ("productos",),)
        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES (?, ?)",
                       ("productos", secuencia_original),)
        cursor.execute("""CREATE UNIQUE INDEX indice_productos_nombre_unico
                       ON productos (LOWER(nombre))""")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

if __name__ == "__main__":
    migrar_checks_productos()
    print("Migración completada")

