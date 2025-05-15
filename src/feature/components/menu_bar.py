import flet as ft

class MenuBar(ft.Column):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.width = 200
        self.spacing = 10
    
    def build(self):
        options = [
            ("Início", "home"),
            ("Relatorio PCO", "report_pco"),
            ("Configurações", "settings")
        ]

        for text, route in options:
            self.controls.append(
                ft.ElevatedButton(text=text, on_click=lambda e, r=route: self.on_navigate(r))
            )