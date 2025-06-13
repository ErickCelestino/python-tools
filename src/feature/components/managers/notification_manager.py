import flet as ft

class NotificationManager:
    def __init__(self, page: ft.Page):
        self.page = page

    def show_notification(self, message: str, bgcolor: str = 'green', text_color: str = 'white', duration: int = 3000):
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=text_color),
            bgcolor=bgcolor,
            duration=duration
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
