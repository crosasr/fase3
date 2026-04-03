# ui/formulario.py — Campos y validaciones del formulario

import flet as ft


def crear_campos():
    """Retorna un dict con todos los campos del formulario."""
    return {
        "nombre": ft.TextField(
            label="Nombre del producto",
            expand=True,
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_GREY_700,
        ),
        "categoria": ft.Dropdown(
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
        ),
        "precio": ft.TextField(
            label="Precio", width=140, prefix="$",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_GREY_700,
        ),
        "stock": ft.TextField(
            label="Stock", width=110, suffix="uds",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="0",
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_GREY_700,
        ),
        "error_nombre": ft.Text("", color=ft.Colors.RED_400, size=12),
        "error_precio": ft.Text("", color=ft.Colors.RED_400, size=12),
        "texto_edicion": ft.Text("", color=ft.Colors.BLUE_GREY_700,
                                  size=13, weight=ft.FontWeight.W_500),
    }


def limpiar_campos(campos: dict):
    campos["nombre"].value    = ""
    campos["categoria"].value = None
    campos["precio"].value    = ""
    campos["stock"].value     = "0"
    campos["error_nombre"].value  = ""
    campos["error_precio"].value  = ""
    campos["texto_edicion"].value = ""


def validar(campos: dict):
    """Valida los campos. Retorna (errores[], precio, stock)."""
    campos["error_nombre"].value = ""
    campos["error_precio"].value = ""
    errores = []

    nombre = campos["nombre"].value.strip()
    if not nombre:
        errores.append("Nombre obligatorio")
    elif len(nombre) < 2:
        errores.append("Nombre muy corto")

    precio = None
    precio_s = campos["precio"].value.strip()
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
    stock_s = campos["stock"].value.strip()
    if stock_s:
        try:
            stock = int(stock_s)
            if stock < 0:
                errores.append("Stock no puede ser negativo")
        except ValueError:
            errores.append("Stock inválido")

    if errores:
        campos["error_nombre"].value = next(
            (e for e in errores if "Nombre" in e), ""
        )
        campos["error_precio"].value = next(
            (e for e in errores if "Precio" in e
             or "inválido" in e.lower()), ""
        )

    return errores, precio, stock