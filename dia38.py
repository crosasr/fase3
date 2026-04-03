# dia38.py — Estilo e identidad visual
# Gris neutro + NavigationRail lateral + Theme

import flet as ft
import database as db


def main(page: ft.Page):
    page.title = "Sistema PyME"
    page.window.width  = 1000
    page.window.height = 700
    page.padding = 0

    # ── Tema global ───────────────────────────────────────────
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE_GREY,
        use_material3=True,
    )
    page.bgcolor = ft.Colors.GREY_100

    # ── Estado ────────────────────────────────────────────────
    producto_editando = None
    modo_edicion      = False
    ultimo_eliminado  = None

    # ── Campos del formulario ─────────────────────────────────
    campo_nombre = ft.TextField(
        label="Nombre del producto",
        expand=True,
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_700,
    )
    campo_categoria = ft.Dropdown(
        label="Categoría",
        width=180,
        options=[
            ft.dropdown.Option("Alimentos"),
            ft.dropdown.Option("Bebidas"),
            ft.dropdown.Option("Limpieza"),
            ft.dropdown.Option("Higiene"),
            ft.dropdown.Option("Electrónica"),
            ft.dropdown.Option("Ropa"),
            ft.dropdown.Option("Otros"),
        ],
        border_color=ft.Colors.BLUE_GREY_300,
    )
    campo_precio = ft.TextField(
        label="Precio", width=140, prefix="$",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_700,
    )
    campo_stock = ft.TextField(
        label="Stock", width=110, suffix="uds",
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0",
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_700,
    )

    error_nombre  = ft.Text("", color=ft.Colors.RED_400, size=12)
    error_precio  = ft.Text("", color=ft.Colors.RED_400, size=12)
    texto_edicion = ft.Text("", color=ft.Colors.BLUE_GREY_700, size=13,
                            weight=ft.FontWeight.W_500)

    campo_buscar = ft.TextField(
        label="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_700,
        bgcolor=ft.Colors.WHITE,
    )
    contador = ft.Text("", color=ft.Colors.BLUE_GREY_400, size=12)
    lista    = ft.ListView(spacing=2, divider_thickness=1, expand=True)

    # ── Banner stock crítico ──────────────────────────────────
    banner = ft.Banner(
        bgcolor=ft.Colors.ORANGE_50,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED,
                        color=ft.Colors.ORANGE_700, size=26),
        content=ft.Text("", color=ft.Colors.ORANGE_900),
        actions=[
            ft.TextButton("Ver críticos",
                          on_click=lambda e: ver_stock_critico()),
            ft.TextButton("Cerrar",
                          on_click=lambda e: cerrar_banner()),
        ],
    )

    def actualizar_banner():
        criticos = db.stock_critico()
        if criticos:
            banner.content.value = (
                f"⚠️  {len(criticos)} producto"
                f"{'s' if len(criticos) != 1 else ''} con stock crítico"
            )
            page.banner = banner
            banner.open = True
        else:
            cerrar_banner()
        page.update()

    def cerrar_banner():
        banner.open = False
        page.update()

    def ver_stock_critico():
        cerrar_banner()
        criticos = db.stock_critico()

        def cerrar_bs(e):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Stock crítico", size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_700),
                        ft.Divider(),
                        *[
                            ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.CANCEL if p["stock"] == 0
                                    else ft.Icons.WARNING,
                                    color=ft.Colors.RED_700 if p["stock"] == 0
                                    else ft.Colors.ORANGE_700,
                                ),
                                title=ft.Text(p["nombre"]),
                                trailing=ft.Text(
                                    f"{p['stock']} uds",
                                    color=ft.Colors.RED_700 if p["stock"] == 0
                                    else ft.Colors.ORANGE_700,
                                ),
                            )
                            for p in criticos
                        ],
                        ft.TextButton("Cerrar", on_click=cerrar_bs),
                    ],
                    spacing=4,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )
        page.overlay.append(bs)
        bs.open = True
        page.update()

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
            errores.append("Nombre muy corto")

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

    # ── Tile estilizado ───────────────────────────────────────
    def construir_tile(p):
        stock = p["stock"]
        if stock == 0:
            color = ft.Colors.RED_600
            icono = ft.Icons.CANCEL
        elif stock <= 10:
            color = ft.Colors.ORANGE_600
            icono = ft.Icons.WARNING
        else:
            color = ft.Colors.GREEN_600
            icono = ft.Icons.CHECK_CIRCLE

        pid    = p["id"]
        nombre = p["nombre"]

        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(icono, color=color, size=20),
                title=ft.Text(nombre, weight=ft.FontWeight.W_500, size=14),
                subtitle=ft.Text(
                    f"{p['categoria']} · ID {pid}",
                    color=ft.Colors.BLUE_GREY_400,
                    size=12,
                ),
                trailing=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"${p['precio']:,.2f}",
                                        weight=ft.FontWeight.BOLD,
                                        size=13,
                                        color=ft.Colors.BLUE_GREY_800),
                                ft.Text(f"{stock} uds",
                                        size=11, color=color),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=2, tight=True,
                        ),
                        ft.IconButton(
                            ft.Icons.EDIT_OUTLINED,
                            icon_color=ft.Colors.BLUE_GREY_400,
                            icon_size=18,
                            tooltip="Editar",
                            on_click=lambda e, i=pid, n=nombre: editar_producto(i, n),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_300,
                            icon_size=18,
                            tooltip="Eliminar",
                            on_click=lambda e, i=pid, n=nombre: confirmar_eliminar(i, n),
                        ),
                    ],
                    spacing=0, tight=True,
                ),
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            margin=ft.margin.symmetric(vertical=2),
        )

    # ── Cargar lista ──────────────────────────────────────────
    def cargar_lista(productos=None):
        if productos is None:
            productos = db.obtener_todos()
            campo_buscar.value = ""

        lista.controls.clear()

        if not productos:
            lista.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Sin productos — agrega el primero",
                        color=ft.Colors.BLUE_GREY_300,
                        italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=30,
                )
            )
            contador.value = "0 productos"
        else:
            for p in productos:
                lista.controls.append(construir_tile(p))
            n = len(productos)
            contador.value = f"{n} producto{'s' if n != 1 else ''}"

        actualizar_banner()

    # ── Búsqueda ──────────────────────────────────────────────
    def buscar(e):
        termino = campo_buscar.value.strip()
        if termino:
            cargar_lista(db.buscar_por_nombre(termino))
        else:
            cargar_lista()

    campo_buscar.on_change = buscar

    # ── Editar ────────────────────────────────────────────────
    def editar_producto(producto_id, _):
        nonlocal producto_editando, modo_edicion
        producto = db.obtener_por_id(producto_id)
        if producto:
            producto_editando     = producto
            modo_edicion          = True
            campo_nombre.value    = producto["nombre"]
            campo_categoria.value = producto["categoria"]
            campo_precio.value    = str(producto["precio"])
            campo_stock.value     = str(producto["stock"])
            texto_edicion.value   = f"✏️  Editando: {producto['nombre']}"
            page.update()

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

    # ── Eliminar con Deshacer ─────────────────────────────────
    def confirmar_eliminar(producto_id, nombre):
        def eliminar(e):
            nonlocal ultimo_eliminado
            ultimo_eliminado = dict(db.obtener_por_id(producto_id))
            db.eliminar_producto(producto_id)
            bs.open = False
            cargar_lista()

            def deshacer(e):
                if ultimo_eliminado:
                    db.agregar_producto(
                        ultimo_eliminado["nombre"],
                        ultimo_eliminado["categoria"],
                        ultimo_eliminado["precio"],
                        ultimo_eliminado["stock"],
                    )
                    bs_deshacer.open = False
                    cargar_lista()
                    page.update()

            def ignorar(e):
                bs_deshacer.open = False
                page.update()

            bs_deshacer = ft.BottomSheet(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text(f"🗑️  '{nombre}' eliminado",
                                    size=15, weight=ft.FontWeight.W_500),
                            ft.Divider(),
                            ft.Row(controls=[
                                ft.TextButton("Ignorar", on_click=ignorar),
                                ft.TextButton(
                                    "↩️  Deshacer",
                                    on_click=deshacer,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.BLUE_GREY_700
                                    ),
                                ),
                            ]),
                        ],
                        spacing=8, tight=True,
                    ),
                ),
            )
            page.overlay.append(bs_deshacer)
            bs_deshacer.open = True
            page.update()

        def cancelar(e):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("¿Eliminar producto?", size=18,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(f"'{nombre}' será eliminado permanentemente.",
                                color=ft.Colors.BLUE_GREY_500),
                        ft.Divider(),
                        ft.Row(controls=[
                            ft.TextButton("Cancelar", on_click=cancelar),
                            ft.TextButton(
                                "Eliminar",
                                on_click=eliminar,
                                style=ft.ButtonStyle(color=ft.Colors.RED_600),
                            ),
                        ]),
                    ],
                    spacing=8, tight=True,
                ),
            ),
        )
        page.overlay.append(bs)
        bs.open = True
        page.update()

    # ── Guardar ───────────────────────────────────────────────
    def guardar(e):
        errores, precio, stock = validar()

        if errores:
            error_nombre.value = next(
                (err for err in errores if "Nombre" in err), ""
            )
            error_precio.value = next(
                (err for err in errores if "Precio" in err
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
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Actualizado" if exito else "❌ Error al actualizar")
            )
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

    # ── Vistas del NavigationRail ─────────────────────────────
    def vista_inventario():
        return ft.Column(
            controls=[
                ft.Text("Inventario", size=22, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_800),
                ft.Divider(height=12),

                # Formulario
                ft.Container(
                    content=ft.Column(
                        controls=[
                            texto_edicion,
                            ft.Row(controls=[
                                ft.Column(controls=[campo_nombre, error_nombre],
                                          expand=True),
                                ft.Column(controls=[campo_categoria], width=180),
                                ft.Column(controls=[campo_precio, error_precio],
                                          width=140),
                                ft.Column(controls=[campo_stock], width=110),
                            ]),
                            ft.TextButton("Guardar",
                                         icon=ft.Icons.SAVE,
                                         on_click=guardar),
                        ],
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    padding=16,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                ),
                ft.Divider(height=12),

                ft.Row(controls=[campo_buscar, contador],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=6),
                lista,
            ],
            expand=True,
            spacing=0,
        )

    def vista_reporte():
        r = db.resumen_inventario()
        criticos = db.stock_critico()

        def tarjeta(titulo, valor, color=ft.Colors.BLUE_GREY_800):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(titulo, size=12,
                                color=ft.Colors.BLUE_GREY_400),
                        ft.Text(str(valor), size=22,
                                weight=ft.FontWeight.BOLD, color=color),
                    ],
                    spacing=4,
                    tight=True,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=16,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.GREY_200),
                expand=True,
            )

        return ft.Column(
            controls=[
                ft.Text("Reporte de inventario", size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_800),
                ft.Divider(height=12),
                ft.Row(controls=[
                    tarjeta("Productos", r["total_productos"]),
                    tarjeta("Unidades", f"{r['total_unidades']:,}"),
                    tarjeta("Valor total",
                            f"${r['valor_total']:,.2f}",
                            ft.Colors.GREEN_700),
                    tarjeta("Precio promedio",
                            f"${r['precio_promedio']:,.2f}"),
                ], spacing=12),
                ft.Divider(height=16),
                ft.Text("Stock crítico", size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.RED_700),
                ft.ListView(
                    controls=[
                        ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.CANCEL if p["stock"] == 0
                                    else ft.Icons.WARNING,
                                    color=ft.Colors.RED_600 if p["stock"] == 0
                                    else ft.Colors.ORANGE_600,
                                ),
                                title=ft.Text(p["nombre"]),
                                trailing=ft.Text(
                                    f"{p['stock']} uds",
                                    color=ft.Colors.RED_600 if p["stock"] == 0
                                    else ft.Colors.ORANGE_600,
                                ),
                            ),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=8,
                            margin=ft.margin.symmetric(vertical=2),
                        )
                        for p in criticos
                    ] if criticos else [
                        ft.Text("✅ Sin productos críticos",
                                color=ft.Colors.GREEN_600)
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    # ── Contenido principal ───────────────────────────────────
    contenido = ft.Container(
        content=vista_inventario(),
        expand=True,
        padding=20,
        bgcolor=ft.Colors.GREY_100,
    )

    # ── NavigationRail ────────────────────────────────────────
    def cambiar_vista(e):
        idx = e.control.selected_index
        if idx == 0:
            contenido.content = vista_inventario()
            cargar_lista()
        elif idx == 1:
            contenido.content = vista_reporte()
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=80,
        bgcolor=ft.Colors.WHITE,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label="Inventario",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BAR_CHART_OUTLINED,
                selected_icon=ft.Icons.BAR_CHART,
                label="Reporte",
            ),
        ],
        on_change=cambiar_vista,
    )

    # ── Layout principal ──────────────────────────────────────
    page.add(
        ft.Row(
            controls=[
                rail,
                ft.VerticalDivider(width=1, color=ft.Colors.GREY_200),
                contenido,
            ],
            expand=True,
            spacing=0,
        )
    )

    db.init_db()
    cargar_lista()


ft.run(main)