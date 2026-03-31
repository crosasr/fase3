# dia32.py — Conectar Flet con SQLite Parte 2
# Lista que carga productos de la BD + búsqueda en tiempo real

import flet as ft
import database as db


def main(page: ft.Page):
    page.title = "Inventario PyME — Día 32"
    page.window.width = 850
    page.window.height = 650
    page.padding = 20

    # ── Campos formulario ─────────────────────────────────────
    campo_nombre    = ft.TextField(label="Nombre", expand=True)
    campo_categoria = ft.TextField(label="Categoría", width=180)
    campo_precio    = ft.TextField(label="Precio", width=130, prefix="$")
    campo_stock     = ft.TextField(label="Stock", width=100)

    # ── Búsqueda ──────────────────────────────────────────────
    campo_buscar = ft.TextField(
        label="Buscar producto",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
    )

    # ── Contador ──────────────────────────────────────────────
    contador = ft.Text("", color=ft.Colors.GREY_600, size=13)

    # ── Lista ─────────────────────────────────────────────────
    lista = ft.ListView(spacing=4, divider_thickness=1, expand=True)

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

        return ft.ListTile(
            leading=ft.Icon(icono, color=color),
            title=ft.Text(p["nombre"], weight=ft.FontWeight.W_500),
            subtitle=ft.Text(
                f"{p['categoria']} · ID: {p['id']}",
                color=ft.Colors.GREY_600
            ),
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

    # ── Cargar lista ──────────────────────────────────────────
    def cargar_lista(productos=None):
        if productos is None:
            productos = db.obtener_todos()

        lista.controls.clear()

        if not productos:
            lista.controls.append(
                ft.ListTile(
                    title=ft.Text(
                        "Sin resultados",
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

    # ── Búsqueda en tiempo real ───────────────────────────────
    def buscar(e):
        termino = campo_buscar.value.strip()
        if termino:
            resultados = db.buscar_por_nombre(termino)
        else:
            resultados = db.obtener_todos()
        cargar_lista(resultados)
        page.update()

    campo_buscar.on_change = buscar   # ← se dispara en cada tecla

    # ── Guardar ───────────────────────────────────────────────
    def guardar(e):
        nombre    = campo_nombre.value.strip()
        categoria = campo_categoria.value.strip() or "General"
        precio_s  = campo_precio.value.strip()
        stock_s   = campo_stock.value.strip()

        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre obligatorio"))
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

        nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)

        campo_nombre.value    = ""
        campo_categoria.value = ""
        campo_precio.value    = ""
        campo_stock.value     = ""
        campo_buscar.value    = ""   # limpiar búsqueda al guardar

        cargar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ '{nombre}' guardado — ID: {nuevo_id}")
        )
        page.snack_bar.open = True
        page.update()

    # ── Reporte rápido ────────────────────────────────────────
    def mostrar_reporte(e):
        r = db.resumen_inventario()
        criticos = db.stock_critico()

        def cerrar(e):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Reporte de inventario",
                                size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Text(f"📦 Productos: {r['total_productos']}"),
                        ft.Text(f"📊 Unidades: {r['total_unidades']:,}"),
                        ft.Text(f"💰 Valor total: ${r['valor_total']:,.2f}"),
                        ft.Text(f"📈 Precio promedio: ${r['precio_promedio']:,.2f}"),
                        ft.Divider(),
                        ft.Text(
                            f"🔴 Stock crítico: {len(criticos)} productos",
                            color=ft.Colors.RED_700 if criticos else ft.Colors.GREEN_700,
                        ),
                        ft.TextButton("Cerrar", on_click=cerrar),
                    ],
                    spacing=8,
                    tight=True,
                ),
            ),
        )

        page.overlay.append(bs)
        bs.open = True
        page.update()
        
    def test_dialogo(e):
        def cerrar(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Test"),
            content=ft.Text("¿Funciona el diálogo?"),
            actions=[ft.TextButton("Cerrar", on_click=cerrar)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    # ── Layout ────────────────────────────────────────────────
    page.add(
        ft.Text("Sistema de Inventario", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Día 32 — Lista dinámica + búsqueda", size=13,
                color=ft.Colors.GREY_500),
        ft.Divider(height=12),

        # Formulario
        ft.Row(controls=[campo_nombre, campo_categoria,
                         campo_precio, campo_stock]),
        ft.Row(controls=[
            ft.TextButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ft.TextButton("Reporte", icon=ft.Icons.BAR_CHART, on_click=mostrar_reporte),
        ]), 
        ft.Divider(height=12),

        # Búsqueda + contador
        ft.Row(controls=[campo_buscar, contador],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=8),

        # Lista
        lista,
        
        ft.TextButton("TEST", on_click=test_dialogo)
    )

    db.init_db()
    cargar_lista()
    page.update()


ft.run(main)