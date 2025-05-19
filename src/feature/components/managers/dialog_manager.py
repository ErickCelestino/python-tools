import flet as ft
from typing import Optional, List, Callable

class DialogManager:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def create_dialog(
        self,
        title: str,
        content: ft.Control,
        actions: List[ft.Control],
        on_dismiss: Optional[Callable] = None
    ) -> ft.CupertinoAlertDialog:
        dialog = ft.CupertinoAlertDialog(
            title=ft.Text(title),
            content=content,
            actions=actions,
        )
        self.page.overlay.append(dialog)
        return dialog
    
    def show_dialog(self, dialog: ft.CupertinoAlertDialog) -> None:
        dialog.open = True
        self.page.update()
    
    def dismiss_dialog(self, dialog: ft.CupertinoAlertDialog, e: ft.ControlEvent) -> None:
        dialog.open = False
        e.control.page.update()