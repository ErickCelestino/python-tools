import flet as ft

class ThemeManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.theme_button = ft.TextButton(
            text='Escuro',
            icon=ft.Icons.DARK_MODE,
            on_click=self.toggle_theme
        )
        self.colors = [
            {"name": "Roxo", "value": "#6200EE"},
            {"name": "Azul", "value": "#2962FF"},
            {"name": "Verde", "value": "#00C853"},
            {"name": "Vermelho", "value": "#D50000"},
            {"name": "Laranja", "value": "#FF6D00"},
        ]
        self.page.theme = ft.Theme(color_scheme_seed=self.colors[0]["value"])
    
    def change_color(self, selected_color):
        self.page.theme = ft.Theme(color_scheme_seed=selected_color)
        self.page.update()
    
    def toggle_theme(self, e=None):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            if self.theme_button:
                self.theme_button.icon = ft.Icons.DARK_MODE
                self.theme_button.text = 'Escuro'
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            if self.theme_button:
                self.theme_button.icon = ft.Icons.LIGHT_MODE
                self.theme_button.text = 'Claro'

        self.page.update()
    
    def get_theme_control(self):
        button = ft.PopupMenuButton(
            icon=ft.Icons.COLOR_LENS,
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=color["value"]),
                            ft.Text(color["name"])
                        ]
                    ),
                    on_click=lambda e, color=color: self.change_color(color["value"])
                )
                for color in self.colors
            ]
        )
        
        color_button = ft.Row(
            controls=[
                button,
                ft.Text('Cores')
            ],
            width=100
        )

        return ft.Column(
            controls=[
                self.theme_button,
                color_button
            ],
        )
