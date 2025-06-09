import json
import os
import flet as ft

class ThemeManager:
    def __init__(self, page: ft.Page, data_dir: str):
        self.page = page
        self.data_dir = data_dir
        self.data_file = os.path.join(self.data_dir, "settings.json")
        self.colors = [
            {"name": "Roxo", "value": "#6200EE"},
            {"name": "Azul", "value": "#2962FF"},
            {"name": "Verde", "value": "#00C853"},
            {"name": "Vermelho", "value": "#D50000"},
            {"name": "Laranja", "value": "#FF6D00"},
        ]
        self.selected_color = self.colors[0]["value"]
        self.theme_mode = ft.ThemeMode.DARK
        
        self.load_settings()
        
        self.page.theme_mode = self.theme_mode
        self.page.theme = ft.Theme(color_scheme_seed=self.selected_color)
        
        self.theme_button = ft.TextButton(
            text='Claro' if self.theme_mode == ft.ThemeMode.LIGHT else 'Escuro',
            icon=ft.Icons.LIGHT_MODE if self.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE,
            on_click=self.toggle_theme
        )
        
        self.page.update()
    
    def load_settings(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    settings = json.load(f)
                    self.theme_mode = ft.ThemeMode(settings.get("theme_mode", "dark"))
                    self.selected_color = settings.get("color", self.selected_color)
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
    
    def save_settings(self):
        settings = {
            "theme_mode": self.theme_mode.value,
            "color": self.selected_color
        }
        with open(self.data_file, "w") as f:
            json.dump(settings, f)
    
    def change_color(self, selected_color):
        self.selected_color = selected_color
        self.page.theme = ft.Theme(color_scheme_seed=selected_color)
        self.page.update()
        self.save_settings()
    
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
        self.theme_mode = self.page.theme_mode
        self.save_settings()
    
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
