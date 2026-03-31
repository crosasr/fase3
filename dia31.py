# dia31.py — Conectar Flet con SQLite Parte 1
# Botón Guardar que inserta en BD real + lista que se actualiza

import flet as ft
import database as db


def main(page: ft.Page):
    page.title = "Inventario PyME — Día 31"
    page.window.width = 800
    page.window.height = 600
    page.padding = 20

    # ── Campos del formulario ─────────────────────────────────
    campo_nombre    = ft.TextField(label="Nombre", expand=True)
    campo_categoria = ft.TextField(label="Categoría", width=180)
    campo_precio    = ft.TextField(label="Precio", width=130, prefix="$")
    campo_stock     = ft.TextField(label="Stock", width=100)

    # ── Lista de productos ────────────────────────────────────
    lista = ft.ListView(spacing=4, divider_thickness=1, expand=True)

    # ── Cargar productos desde SQLite ─────────────────────────
    def cargar_lista():
        lista.controls.clear()
        productos = db.obtener_todos()

        if not productos:
            lista.controls.append(
                ft.ListTile(title=ft.Text("Sin productos aún — agrega el primero"))
            )
            return

        for p in productos:
            stock = p["stock"]
            if stock == 0:
                color = ft.Colors.RED_700
                icono = ft.Icons.CANCEL
            elif stock <= 10:
                color = ft.Colors.ORANGE_700
                icono = ft.Icons.WARNING
            else:
                color = ft.Colors.GREEN_700
                icono = ft.Icons.CHECK_CIRCLE

            lista.controls.append(
                ft.ListTile(
                    leading=ft.Icon(icono, color=color),
                    title=ft.Text(p["nombre"], weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(p["categoria"], color=ft.Colors.GREY_600),
                    trailing=ft.Column(
                        controls=[
                            ft.Text(f"${p['precio']:,.2f}",
                                    weight=ft.FontWeight.BOLD, size=13),
                            ft.Text(f"{stock} uds", size=12, color=color),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=2,
                        tight=True,
                    ),
                )
            )

    # ── Evento guardar ────────────────────────────────────────
    def guardar(e):
        nombre    = campo_nombre.value.strip()
        categoria = campo_categoria.value.strip() or "General"
        precio_s  = campo_precio.value.strip()
        stock_s   = campo_stock.value.strip()

        # Validación
        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El nombre es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            precio = float(precio_s.replace(",", "."))
            stock  = int(stock_s) if stock_s else 0
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Precio o stock inválido"))
            page.snack_bar.open = True
            page.update()
            return

        # Insertar en SQLite
        nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)

        # Limpiar campos
        campo_nombre.value    = ""
        campo_categoria.value = ""
        campo_precio.value    = ""
        campo_stock.value     = ""

        # Recargar lista desde BD
        cargar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ '{nombre}' guardado — ID: {nuevo_id}")
        )
        page.snack_bar.open = True
        page.update()

    # ── Layout ────────────────────────────────────────────────
    page.add(
        ft.Text("Sistema de Inventario", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Día 31 — Flet + SQLite conectados", size=13,
                color=ft.Colors.GREY_500),
        ft.Divider(height=12),

        # Formulario
        ft.Row(controls=[campo_nombre, campo_categoria,
                         campo_precio, campo_stock]),
        ft.ElevatedButton("Guardar producto", icon=ft.Icons.SAVE,
                          on_click=guardar),
        ft.Divider(height=12),

        # Lista
        ft.Text("Productos en BD", size=16, weight=ft.FontWeight.W_500),
        lista,
    )

    # Cargar productos al iniciar
    db.init_db()
    cargar_lista()
    page.update()


ft.run(main)