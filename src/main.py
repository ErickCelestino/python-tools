import flet as ft
from dotenv import load_dotenv
from app import App
from feature.components.managers import ThemeManager

def main(page: ft.Page):
    load_dotenv()
    dir = 'data'
    page.title = 'Vitru dev Tools'
    page.window.maximized = True
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    ThemeManager(page, dir)
    
    app = App(page, dir)
    page.add(app)

ft.app(target=main)
