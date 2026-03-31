# database.py — Capa de datos reutilizable
# Se importa igual en Fase 3 (Flet) sin modificaciones

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tienda.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre    TEXT    NOT NULL,
                categoria TEXT    NOT NULL DEFAULT 'General',
                precio    REAL    NOT NULL,
                stock     INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()


def agregar_producto(nombre, categoria, precio, stock):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (nombre.strip(), categoria.strip(), precio, stock)
        )
        conn.commit()
        return cursor.lastrowid


def obtener_todos():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos ORDER BY nombre ASC"
        ).fetchall()


def obtener_por_id(producto_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE id = ?", (producto_id,)
        ).fetchone()


def buscar_por_nombre(termino):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre",
            (f"%{termino}%",)
        ).fetchall()


def actualizar_producto(pid, nombre, categoria, precio, stock):
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE productos
               SET nombre = ?, categoria = ?, precio = ?, stock = ?
               WHERE id = ?""",
            (nombre.strip(), categoria.strip(), precio, stock, pid)
        )
        conn.commit()
        return cursor.rowcount > 0


def eliminar_producto(pid):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM productos WHERE id = ?", (pid,)
        )
        conn.commit()
        return cursor.rowcount > 0


def stock_critico(umbral=10):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE stock <= ? ORDER BY stock ASC",
            (umbral,)
        ).fetchall()


def resumen_inventario():
    with get_connection() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*)                     AS total_productos,
                COALESCE(SUM(stock), 0)          AS total_unidades,
                COALESCE(SUM(precio * stock), 0) AS valor_total,
                COALESCE(AVG(precio), 0)          AS precio_promedio
            FROM productos
        """).fetchone()
        return dict(row)