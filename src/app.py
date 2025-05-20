import flet as ft
from feature.pages import HomePage, PcoReport
from feature.components.menu_bar import MenuBar
from feature.components.managers import NotificationManager

class App(ft.Row):
    def __init__(self, page: ft.Page, data_dir):
        super().__init__()
        self.page = page
        self.expand = True
        self.data_dir = data_dir
        self.notification = NotificationManager(self.page)
        self.render()

    def navigate(self, route: str):
        if route == "home":
            self.container_content.content = HomePage()
        elif route == "report_pco":
            self.container_content.content = PcoReport(notification=self.notification,page=self.page, data_dir=self.data_dir)
        self.page.update()

    def render(self):
        self.menu = MenuBar(on_navigate=self.navigate)
        self.container_content = ft.Container(expand=True)

        self.controls = [
            self.menu,
            ft.VerticalDivider(width=1),
            self.container_content
        ]

        self.navigate("home")
    