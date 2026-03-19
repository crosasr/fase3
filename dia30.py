import flet as ft

def main(page: ft.Page):
    page.title = "Inventario"
    page.padding = 20

    # Datos de prueba — en Día 31 vienen de SQLite
    productos = [
        {"nombre": "Silla",      "categoria": "Muebles",   "precio": 1350.00, "stock": 15},
        {"nombre": "Mesa",       "categoria": "Muebles",   "precio": 2800.00, "stock": 8},
        {"nombre": "Escritorio", "categoria": "Muebles",   "precio": 3200.00, "stock": 3},
        {"nombre": "Archivero",  "categoria": "Oficina",   "precio": 1800.00, "stock": 0},
        {"nombre": "Sillón",     "categoria": "Muebles",   "precio": 4500.00, "stock": 5},
        {"nombre": "Librero",    "categoria": "Muebles",   "precio": 2100.00, "stock": 12},
    ]

    def color_stock(stock):
        if stock == 0:   return ft.Colors.RED_700
        if stock <= 5:   return ft.Colors.ORANGE_700
        return ft.Colors.GREEN_700

    def icono_stock(stock):
        if stock == 0:   return ft.Icons.CANCEL
        if stock <= 5:   return ft.Icons.WARNING
        return ft.Icons.CHECK_CIRCLE

    def construir_tile(p):
        return ft.ListTile(
            leading=ft.Icon(
                ft.Icons.CHAIR,
                color=color_stock(p["stock"])
            ),
            title=ft.Text(p["nombre"], weight=ft.FontWeight.W_500),
            subtitle=ft.Text(p["categoria"], color=ft.Colors.GREY_600),
            trailing=ft.Column(
                controls=[
                    ft.Text(f"${p['precio']:,.2f}", size=13,
                            weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            ft.Icon(icono_stock(p["stock"]),
                                    size=14,
                                    color=color_stock(p["stock"])),
                            ft.Text(f"{p['stock']} uds",
                                    size=12,
                                    color=color_stock(p["stock"])),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=2,
                tight=True,
            ),
        )

    lista = ft.ListView(
        controls=[construir_tile(p) for p in productos],
        spacing=4,
        divider_thickness=1,   # ← línea separadora entre ítems
        expand=True,
    )

    page.add(
        ft.Text("Inventario", size=22, weight=ft.FontWeight.BOLD),
        ft.Text(f"{len(productos)} productos", color=ft.Colors.GREY_500),
        ft.Divider(),
        lista,
    )

ft.run(main)