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
        return self.theme_button
