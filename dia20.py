# dia20.py — Conceptos base de Flet
# Page, controls, layout, eventos, feedback

import flet as ft


def main(page: ft.Page):
    page.title = "Sistema PyME — Día 20"
    page.window.width = 700
    page.window.height = 500
    page.padding = 30

    # ── Controles ────────────────────────────────────────────
    campo_nombre  = ft.TextField(label="Nombre del producto", width=350)
    campo_precio  = ft.TextField(label="Precio", width=160, prefix="$")
    campo_stock   = ft.TextField(label="Stock", width=120, suffix="uds")
    lista_productos = ft.Column(spacing=4)

    contador = ft.Text("0 productos agregados", color=ft.Colors.GREY_600)

    # ── Evento guardar ────────────────────────────────────────
    def guardar(e):
        nombre = campo_nombre.value.strip()
        precio = campo_precio.value.strip()
        stock  = campo_stock.value.strip()

        if not nombre or not precio:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre y precio son obligatorios"))
            page.update()
            return

        # Agregar a la lista visual
        lista_productos.controls.append(
            ft.Text(f"• {nombre}  —  ${float(precio):,.2f}  ×  {stock or 0} uds")
        )

        # Actualizar contador
        n = len(lista_productos.controls)
        contador.value = f"{n} producto{'s' if n != 1 else ''} agregado{'s' if n != 1 else ''}"

        # Limpiar campos
        campo_nombre.value = ""
        campo_precio.value = ""
        campo_stock.value  = ""

        page.snack_bar = ft.SnackBar(ft.Text(f"✅ '{nombre}' agregado"))
        page.update()

    def limpiar(e):
        lista_productos.controls.clear()
        contador.value = "0 productos agregados"
        page.update()

    # ── Layout ────────────────────────────────────────────────
    page.add(
        ft.Text("Sistema de Inventario", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Día 20 — Flet básico", size=13, color=ft.Colors.GREY_500),
        ft.Divider(height=16),

        ft.Row(controls=[campo_nombre, campo_precio, campo_stock]),

        ft.Row(controls=[
            ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ft.OutlinedButton("Limpiar lista", icon=ft.Icons.DELETE_SWEEP, on_click=limpiar),
        ]),

        ft.Divider(height=16),
        contador,
        lista_productos,
    )


ft.run(main)