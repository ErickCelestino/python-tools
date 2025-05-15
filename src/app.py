import flet as ft
from feature.pages import HomePage
from feature.components.menu_bar import MenuBar

class App(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.render()

    def navigate(self, route: str):
        if route == "home":
            self.container_content.content = HomePage()
        elif route == "report_pco":
            self.container_content.content = HomePage()
        self.page.update()

    def render(self):
        self.menu = MenuBar(on_navigate=self.navigate)
        self.container_content = ft.Container(expand=True)

        self.controls = [
            self.menu,
            self.container_content
        ]

        self.navigate("home")
    