# ui/vistas.py — Vistas de la aplicación

from flet import Border, Margin
import flet as ft
import database as db
from ui.componentes import construir_tile, construir_tarjeta
from ui.formulario  import crear_campos, limpiar_campos, validar


def crear_vista_inventario(page: ft.Page):
    """Retorna (vista, cargar_lista) para la vista de inventario."""

    estado = {
        "producto_editando": None,
        "modo_edicion":      False,
        "ultimo_eliminado":  None,
    }

    campos  = crear_campos()
    lista   = ft.ListView(spacing=2, divider_thickness=1, expand=True)
    contador = ft.Text("", color=ft.Colors.BLUE_GREY_400, size=12)
    campo_buscar = ft.TextField(
        label="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_700,
        bgcolor=ft.Colors.WHITE,
    )

    # ── Banner ────────────────────────────────────────────────
    banner = ft.Banner(
        bgcolor=ft.Colors.ORANGE_50,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED,
                        color=ft.Colors.ORANGE_700, size=26),
        content=ft.Text("", color=ft.Colors.ORANGE_900),
        actions=[
            ft.TextButton("Cerrar",
                          on_click=lambda e: _cerrar_banner()),
        ],
    )

    def _cerrar_banner():
        banner.open = False
        page.update()

    def _actualizar_banner():
        criticos = db.stock_critico()
        if criticos:
            banner.content.value = (
                f"⚠️  {len(criticos)} producto"
                f"{'s' if len(criticos) != 1 else ''} con stock crítico"
            )
            page.banner = banner
            banner.open = True
        else:
            _cerrar_banner()
        page.update()

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
                lista.controls.append(
                    construir_tile(p, _editar, _confirmar_eliminar)
                )
            n = len(productos)
            contador.value = f"{n} producto{'s' if n != 1 else ''}"

        _actualizar_banner()

    # ── Búsqueda ──────────────────────────────────────────────
    def _buscar(e):
        termino = campo_buscar.value.strip()
        if termino:
            cargar_lista(db.buscar_por_nombre(termino))
        else:
            cargar_lista()

    campo_buscar.on_change = _buscar

    # ── Editar ────────────────────────────────────────────────
    def _editar(producto_id, _):
        producto = db.obtener_por_id(producto_id)
        if producto:
            estado["producto_editando"] = producto
            estado["modo_edicion"]      = True
            campos["nombre"].value      = producto["nombre"]
            campos["categoria"].value   = producto["categoria"]
            campos["precio"].value      = str(producto["precio"])
            campos["stock"].value       = str(producto["stock"])
            campos["texto_edicion"].value = f"✏️  Editando: {producto['nombre']}"
            page.update()

    def _resetear_edicion():
        estado["producto_editando"] = None
        estado["modo_edicion"]      = False
        limpiar_campos(campos)
        page.update()

    # ── Eliminar con Deshacer ─────────────────────────────────
    def _confirmar_eliminar(producto_id, nombre):
        def eliminar(e):
            estado["ultimo_eliminado"] = dict(db.obtener_por_id(producto_id))
            db.eliminar_producto(producto_id)
            bs.open = False
            cargar_lista()

            def deshacer(e):
                u = estado["ultimo_eliminado"]
                if u:
                    db.agregar_producto(u["nombre"], u["categoria"],
                                        u["precio"], u["stock"])
                    bs2.open = False
                    cargar_lista()
                    page.update()

            def ignorar(e):
                bs2.open = False
                page.update()

            bs2 = ft.BottomSheet(
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
            page.overlay.append(bs2)
            bs2.open = True
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
    def _guardar(e):
        errores, precio, stock = validar(campos)

        if errores:
            page.update()
            return

        nombre    = campos["nombre"].value.strip()
        categoria = campos["categoria"].value or "Otros"

        if estado["modo_edicion"]:
            exito = db.actualizar_producto(
                estado["producto_editando"]["id"],
                nombre, categoria, precio, stock
            )
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Actualizado" if exito else "❌ Error")
            )
            page.snack_bar.open = True
            _resetear_edicion()
        else:
            nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ '{nombre}' guardado — ID: {nuevo_id}")
            )
            page.snack_bar.open = True

        cargar_lista()
        page.update()

    # ── Vista ─────────────────────────────────────────────────
    vista = ft.Column(
        controls=[
            ft.Text("Inventario", size=22, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_800),
            ft.Divider(height=12),
            ft.Container(
                content=ft.Column(
                    controls=[
                        campos["texto_edicion"],
                        ft.Row(controls=[
                            ft.Column(controls=[
                                campos["nombre"],
                                campos["error_nombre"],
                            ], expand=True),
                            ft.Column(controls=[campos["categoria"]], width=180),
                            ft.Column(controls=[
                                campos["precio"],
                                campos["error_precio"],
                            ], width=140),
                            ft.Column(controls=[campos["stock"]], width=110),
                        ]),
                        ft.TextButton("Guardar",
                                      icon=ft.Icons.SAVE,
                                      on_click=_guardar),
                    ],
                    spacing=8,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=16,
                border_radius=10,
                border=Border.all(1, ft.Colors.GREY_200),
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

    return vista, cargar_lista


def crear_vista_reporte():
    """Retorna la vista de reporte con métricas y stock crítico."""
    r        = db.resumen_inventario()
    criticos = db.stock_critico()

    return ft.Column(
        controls=[
            ft.Text("Reporte de inventario", size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_800),
            ft.Divider(height=12),
            ft.Row(controls=[
                construir_tarjeta("Productos",
                                   str(r["total_productos"])),
                construir_tarjeta("Unidades",
                                   f"{r['total_unidades']:,}"),
                construir_tarjeta("Valor total",
                                   f"${r['valor_total']:,.2f}",
                                   ft.Colors.GREEN_700),
                construir_tarjeta("Precio promedio",
                                   f"${r['precio_promedio']:,.2f}"),
            ], spacing=12),
            ft.Divider(height=16),
            ft.Text("Stock crítico", size=16, weight=ft.FontWeight.W_500,
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
                        margin=Margin.symmetric(vertical=2),
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