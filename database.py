# database.py — Capa de datos reutilizable
# Fase 2 | Día 19 — Este archivo se importa igual en Fase 3 (Flet)

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tienda.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ← acceso por nombre de columna
    return conn


def init_db():
    """Crea las tablas si no existen. Llamar al arrancar la app."""
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


# ── CRUD ──────────────────────────────────────────────────────

def agregar_producto(nombre: str, categoria: str, precio: float, stock: int) -> int:
    """Retorna el id del nuevo registro."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (nombre.strip(), categoria.strip(), precio, stock)
        )
        conn.commit()
        return cursor.lastrowid  # ← id generado por AUTOINCREMENT


def obtener_todos() -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos ORDER BY nombre ASC"
        ).fetchall()


def obtener_por_id(producto_id: int):
    """Retorna un Row o None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE id = ?", (producto_id,)
        ).fetchone()


def buscar_por_nombre(termino: str) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre",
            (f"%{termino}%",)
        ).fetchall()


def actualizar_producto(pid: int, nombre: str, categoria: str,
                        precio: float, stock: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE productos
               SET nombre = ?, categoria = ?, precio = ?, stock = ?
               WHERE id = ?""",
            (nombre.strip(), categoria.strip(), precio, stock, pid)
        )
        conn.commit()
        return cursor.rowcount > 0  # ← True si modificó algo


def eliminar_producto(pid: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM productos WHERE id = ?", (pid,)
        )
        conn.commit()
        return cursor.rowcount > 0


# ── Reportes ──────────────────────────────────────────────────

def stock_critico(umbral: int = 10) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE stock <= ? ORDER BY stock ASC",
            (umbral,)
        ).fetchall()


def resumen_inventario() -> dict:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*)            AS total_productos,
                COALESCE(SUM(stock), 0)          AS total_unidades,
                COALESCE(SUM(precio * stock), 0) AS valor_total,
                COALESCE(AVG(precio), 0)          AS precio_promedio
            FROM productos
        """).fetchone()
        return dict(row)  # ← Row → dict para fácil consumo en Flet