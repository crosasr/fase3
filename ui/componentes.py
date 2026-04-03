# ui/componentes.py — Controles reutilizables
# Tiles, tarjetas y elementos visuales independientes de la lógica

from flet import Border, Margin
import flet as ft


def color_stock(stock: int) -> str:
    if stock == 0:   return ft.Colors.RED_600
    if stock <= 10:  return ft.Colors.ORANGE_600
    return ft.Colors.GREEN_600


def icono_stock(stock: int):
    if stock == 0:   return ft.Icons.CANCEL
    if stock <= 10:  return ft.Icons.WARNING
    return ft.Icons.CHECK_CIRCLE


def construir_tile(p, on_editar, on_eliminar) -> ft.Container:
    stock  = p["stock"]
    pid    = p["id"]
    nombre = p["nombre"]
    color  = color_stock(stock)
    icono  = icono_stock(stock)

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
                            ft.Text(f"{stock} uds", size=11, color=color),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=2,
                        tight=True,
                    ),
                    ft.IconButton(
                        ft.Icons.EDIT_OUTLINED,
                        icon_color=ft.Colors.BLUE_GREY_400,
                        icon_size=18,
                        tooltip="Editar",
                        on_click=lambda e, i=pid, n=nombre: on_editar(i, n),
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_300,
                        icon_size=18,
                        tooltip="Eliminar",
                        on_click=lambda e, i=pid, n=nombre: on_eliminar(i, n),
                    ),
                ],
                spacing=0,
                tight=True,
            ),
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        margin=Margin.symmetric(vertical=2),
    )


def construir_tarjeta(titulo: str, valor: str,
                      color=ft.Colors.BLUE_GREY_800) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=12, color=ft.Colors.BLUE_GREY_400),
                ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=16,
        border_radius=10,
        border=Border.all(1, ft.Colors.GREY_200),
        expand=True,
    )