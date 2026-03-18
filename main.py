import flet as ft
import database as db


def main(page: ft.Page):
    db.init_db()
    page.title = "Sistema PyME"
    page.add(ft.Text("Fase 3 — ¡Flet funcionando! 🎉"))


ft.run(main)