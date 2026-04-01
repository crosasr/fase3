# dia34.py — Validaciones en formulario
# Campos obligatorios, tipos correctos, rangos válidos

import flet as ft
import database as db


def main(page: ft.Page):
    page.title = "Inventario PyME — Día 34"
    page.window.width = 850
    page.window.height = 650
    page.padding = 20

    # ── Campos del formulario ─────────────────────────────────
    campo_nombre = ft.TextField(
        label="Nombre del producto",
        expand=True,
    )
    campo_categoria = ft.TextField(
        label="Categoría",
        width=180,
        value="General",
    )
    campo_precio = ft.TextField(
        label="Precio",
        width=140,
        prefix="$",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_stock = ft.TextField(
        label="Stock",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # ── Texto de error visible ────────────────────────────────
    texto_error = ft.Text(
        "",
        color=ft.Colors.RED_700,
        size=13,
        weight=ft.FontWeight.W_500,
    )

    # ── Búsqueda y contador ───────────────────────────────────
    campo_buscar = ft.TextField(
        label="Buscar producto",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
    )
    contador = ft.Text("", color=ft.Colors.GREY_600, size=13)

    # ── Lista ─────────────────────────────────────────────────
    lista = ft.ListView(spacing=4, divider_thickness=1, expand=True)

    # ── Validaciones ──────────────────────────────────────────
    def limpiar_errores():
        campo_nombre.error_text    = None
        campo_categoria.error_text = None
        campo_precio.error_text    = None
        campo_stock.error_text     = None
        texto_error.value          = ""

    def validar():
        limpiar_errores()
        errores = []

        nombre = campo_nombre.value.strip()
        if not nombre:
            errores.append("Nombre obligatorio")
        elif len(nombre) < 2:
            errores.append("Nombre muy corto (mínimo 2 caracteres)")

        precio = None
        precio_s = campo_precio.value.strip()
        if not precio_s:
            errores.append("Precio obligatorio")
        else:
            try:
                precio = float(precio_s.replace(",", "."))
                if precio <= 0:
                    errores.append("Precio debe ser mayor a 0")
            except ValueError:
                errores.append("Precio inválido — ingresa un número")

        stock = 0
        stock_s = campo_stock.value.strip()
        if stock_s:
            try:
                stock = int(stock_s)
                if stock < 0:
                    errores.append("Stock no puede ser negativo")
            except ValueError:
                errores.append("Stock inválido — ingresa un entero")

        return errores, precio, stock

    # ── Construir tile ────────────────────────────────────────
    def construir_tile(p):
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

        pid    = p["id"]
        nombre = p["nombre"]

        return ft.ListTile(
            leading=ft.Icon(icono, color=color),
            title=ft.Text(nombre, weight=ft.FontWeight.W_500),
            subtitle=ft.Text(
                f"{p['categoria']} · ID: {pid}",
                color=ft.Colors.GREY_600,
            ),
            trailing=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(f"${p['precio']:,.2f}",
                                    weight=ft.FontWeight.BOLD, size=13),
                            ft.Text(f"{stock} uds", size=12, color=color),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=2,
                        tight=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Eliminar",
                        on_click=lambda e, i=pid, n=nombre: confirmar_eliminar(i, n),
                    ),
                ],
                spacing=4,
                tight=True,
            ),
        )

    # ── Cargar lista ──────────────────────────────────────────
    def cargar_lista(productos=None):
        if productos is None:
            productos = db.obtener_todos()

        lista.controls.clear()

        if not productos:
            lista.controls.append(
                ft.ListTile(
                    title=ft.Text(
                        "Sin productos — agrega el primero",
                        color=ft.Colors.GREY_500,
                        italic=True,
                    )
                )
            )
            contador.value = "0 productos"
        else:
            for p in productos:
                lista.controls.append(construir_tile(p))
            n = len(productos)
            contador.value = f"{n} producto{'s' if n != 1 else ''}"

        page.update()

    # ── Búsqueda en tiempo real ───────────────────────────────
    def buscar(e):
        termino = campo_buscar.value.strip()
        if termino:
            cargar_lista(db.buscar_por_nombre(termino))
        else:
            cargar_lista()

    campo_buscar.on_change = buscar

    # ── Confirmar eliminar ────────────────────────────────────
    def confirmar_eliminar(producto_id, nombre):
        def eliminar(e):
            db.eliminar_producto(producto_id)
            bs.open = False
            cargar_lista()
            page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ '{nombre}' eliminado"))
            page.snack_bar.open = True
            page.update()

        def cancelar(e):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("¿Eliminar producto?",
                                size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"'{nombre}' será eliminado permanentemente.",
                                color=ft.Colors.GREY_600),
                        ft.Divider(),
                        ft.Row(controls=[
                            ft.TextButton("Cancelar", on_click=cancelar),
                            ft.TextButton(
                                "Eliminar",
                                on_click=eliminar,
                                style=ft.ButtonStyle(color=ft.Colors.RED_700),
                            ),
                        ]),
                    ],
                    spacing=8,
                    tight=True,
                ),
            ),
        )
        page.overlay.append(bs)
        bs.open = True
        page.update()

    # ── Guardar con validación ────────────────────────────────
    def guardar(e):
        errores, precio, stock = validar()

        if errores:
            texto_error.value = "❌ " + " · ".join(errores)
            page.update()
            return

        texto_error.value = ""

        nombre    = campo_nombre.value.strip()
        categoria = campo_categoria.value.strip() or "General"

        nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)

        campo_nombre.value    = ""
        campo_categoria.value = "General"
        campo_precio.value    = ""
        campo_stock.value     = ""
        campo_buscar.value    = ""

        cargar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ '{nombre}' guardado — ID: {nuevo_id}")
        )
        page.snack_bar.open = True
        page.update()

    # ── Layout ────────────────────────────────────────────────
    page.add(
        ft.Text("Sistema de Inventario", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Día 34 — Validaciones en formulario", size=13,
                color=ft.Colors.GREY_500),
        ft.Divider(height=12),

        ft.Row(controls=[campo_nombre, campo_categoria,
                         campo_precio, campo_stock]),
        ft.TextButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
        texto_error,
        ft.Divider(height=12),

        ft.Row(controls=[campo_buscar, contador],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=8),

        lista,
    )

    db.init_db()
    cargar_lista()


ft.run(main)