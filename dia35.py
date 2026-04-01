# dia35.py — Mini-proyecto parte 1 y 2
# Formulario + lista + edición + validaciones

import flet as ft
import database as db


def main(page: ft.Page):
    page.title = "Gestión de Inventario PyME"
    page.window.width = 900
    page.window.height = 700
    page.padding = 20

    # ── Estado de edición ─────────────────────────────────────
    producto_editando = None
    modo_edicion = False

    # ── Campos del formulario ─────────────────────────────────
    campo_nombre = ft.TextField(
        label="Nombre del producto",
        width=300,
        autofocus=True,
    )
    campo_categoria = ft.Dropdown(
        label="Categoría",
        width=200,
        options=[
            ft.dropdown.Option("Alimentos"),
            ft.dropdown.Option("Bebidas"),
            ft.dropdown.Option("Limpieza"),
            ft.dropdown.Option("Higiene"),
            ft.dropdown.Option("Electrónica"),
            ft.dropdown.Option("Ropa"),
            ft.dropdown.Option("Otros"),
        ],
    )
    campo_precio = ft.TextField(
        label="Precio",
        width=150,
        prefix="$",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_stock = ft.TextField(
        label="Stock",
        width=120,
        suffix="uds",
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0",
    )

    # ── Errores e indicador de edición ────────────────────────
    error_nombre  = ft.Text("", color=ft.Colors.RED_500, size=12)
    error_precio  = ft.Text("", color=ft.Colors.RED_500, size=12)
    texto_edicion = ft.Text("", color=ft.Colors.BLUE_600, size=14,
                            weight=ft.FontWeight.BOLD)

    # ── Búsqueda y contador ───────────────────────────────────
    campo_buscar = ft.TextField(
        label="Buscar producto...",
        width=400,
        prefix_icon=ft.Icons.SEARCH,
    )
    contador = ft.Text("0 productos", color=ft.Colors.GREY_600, size=14)

    # ── Lista ─────────────────────────────────────────────────
    lista = ft.ListView(spacing=4, divider_thickness=1, expand=True)

    # ── Validaciones ──────────────────────────────────────────
    def limpiar_errores():
        error_nombre.value = ""
        error_precio.value = ""

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
                errores.append("Precio inválido")

        stock = 0
        stock_s = campo_stock.value.strip()
        if stock_s:
            try:
                stock = int(stock_s)
                if stock < 0:
                    errores.append("Stock no puede ser negativo")
            except ValueError:
                errores.append("Stock inválido")

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
            title=ft.Text(nombre, weight=ft.FontWeight.BOLD),
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
                        ft.Icons.EDIT,
                        icon_color=ft.Colors.BLUE_400,
                        tooltip="Editar",
                        on_click=lambda e, i=pid, n=nombre: editar_producto(i, n),
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
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
            campo_buscar.value = ""   # limpiar búsqueda al recargar completo

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

    # ── Editar producto ───────────────────────────────────────
    def editar_producto(producto_id, nombre):
        nonlocal producto_editando, modo_edicion

        producto = db.obtener_por_id(producto_id)
        if producto:
            producto_editando = producto
            modo_edicion      = True

            campo_nombre.value    = producto["nombre"]
            campo_categoria.value = producto["categoria"]
            campo_precio.value    = str(producto["precio"])
            campo_stock.value     = str(producto["stock"])

            texto_edicion.value = f"✏️ Editando: {producto['nombre']}"
            page.update()

    # ── Resetear modo edición ─────────────────────────────────
    def resetear_edicion():
        nonlocal producto_editando, modo_edicion

        producto_editando     = None
        modo_edicion          = False
        texto_edicion.value   = ""
        campo_nombre.value    = ""
        campo_categoria.value = None
        campo_precio.value    = ""
        campo_stock.value     = "0"
        page.update()

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
            error_nombre.value = next(
                (err for err in errores if "Nombre" in err), ""
            )
            error_precio.value = next(
                (err for err in errores if "Precio" in err or "número" in err
                 or "inválido" in err.lower()), ""
            )
            page.update()
            return

        limpiar_errores()
        nombre    = campo_nombre.value.strip()
        categoria = campo_categoria.value or "Otros"

        if modo_edicion:
            exito = db.actualizar_producto(
                producto_editando["id"], nombre, categoria, precio, stock
            )
            msg = f"✅ '{nombre}' actualizado" if exito else f"❌ Error al actualizar"
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            resetear_edicion()
        else:
            nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ '{nombre}' guardado — ID: {nuevo_id}")
            )
            page.snack_bar.open = True

        cargar_lista()
        page.update()

    # ── Layout ────────────────────────────────────────────────
    page.add(
        ft.Column(
            controls=[
                # Header
                ft.Row(controls=[
                    ft.Text("Gestión de Inventario", size=28,
                            weight=ft.FontWeight.BOLD),
                    ft.Text("PyME Mexicana", size=16,
                            color=ft.Colors.GREY_600),
                ]),
                ft.Divider(height=16),

                # Formulario
                ft.Text("Agregar / Editar Producto", size=18,
                        weight=ft.FontWeight.BOLD),
                texto_edicion,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(controls=[
                                ft.Column(controls=[campo_nombre, error_nombre],
                                          width=300),
                                ft.Column(controls=[campo_categoria], width=200),
                                ft.Column(controls=[campo_precio, error_precio],
                                          width=150),
                                ft.Column(controls=[campo_stock], width=120),
                            ]),
                            ft.TextButton(
                                "Guardar producto",
                                icon=ft.Icons.SAVE,
                                on_click=guardar,
                            ),
                        ],
                    ),
                    padding=15,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                ),
                ft.Divider(height=16),

                # Búsqueda y contador
                ft.Row(
                    controls=[campo_buscar, contador],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=8),

                # Lista
                ft.Text("Lista de Productos", size=18,
                        weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=lista,
                    height=350,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                ),
            ],
        )
    )

    db.init_db()
    cargar_lista()


ft.run(main)