# app.py — Orquestador principal
# NavigationRail + estado global + inicialización

import flet as ft
import database as db
from ui.vistas import crear_vista_inventario, crear_vista_reporte


def main(page: ft.Page):
    page.title   = "Sistema PyME"
    page.window.width  = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_100
    page.theme   = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE_GREY,
        use_material3=True,
    )

    db.init_db()

    # ── Vista inicial ─────────────────────────────────────────
    vista_inv, cargar_lista = crear_vista_inventario(page)

    contenido = ft.Container(
        content=vista_inv,
        expand=True,
        padding=20,
        bgcolor=ft.Colors.GREY_100,
    )

    cargar_lista()

    # ── NavigationRail ────────────────────────────────────────
    def cambiar_vista(e):
        idx = e.control.selected_index
        if idx == 0:
            vista, cargar = crear_vista_inventario(page)
            contenido.content = vista
            cargar()
        elif idx == 1:
            contenido.content = crear_vista_reporte()
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