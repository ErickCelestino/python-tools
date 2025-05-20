import re
import flet as ft
from typing import Optional, Dict, List, Callable
from datetime import datetime
from ..managers import DialogManager

class EmailDialogHandler:
    def __init__(self, page: ft.Page, dialog_manager: DialogManager, refresh_callback: Callable):
        self.page = page
        self.dialog_manager = dialog_manager
        self.refresh_callback = refresh_callback
        self.selected_item: Optional[Dict] = None
    
    def _get_email_modal_content(self, email: Optional[str] = None) -> ft.Container:
        return ft.Container(
            ft.TextField(
                value=email if email else "",
                label="Email",
                autofocus=True
            ),
            height=80,
            alignment=ft.alignment.center,
        )
    
    def valid_email(self, email: str) -> bool:
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(padrao, email) is not None
    
    def _show_error_snackbar(self, message: str) -> None:
        snackbar = ft.SnackBar(
            ft.Text(message, color='white'),
            bgcolor='red'
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    
    def _create_dialog(self, title: str, content: ft.Control, actions: List[ft.Control]) -> ft.Control:
        return self.dialog_manager.create_dialog(
            title=title,
            content=content,
            actions=actions
        )
    
    def _handle_save_email(self, dialog: ft.Control, e: ft.ControlEvent, email: str, email_list: List[Dict], is_edit: bool = False) -> None:
        if not self.valid_email(email):
            self._show_error_snackbar('E-mail inválido!')
            return

        if is_edit and self.selected_item:
            self.selected_item["email"] = email
        else:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            email_list.append({
                'id': str(len(email_list) + 1),
                'created_at': current_time,
                'email': email
            })
        
        self.dialog_manager.dismiss_dialog(dialog, e)
        self.refresh_callback()
    
    def open_add_modal(self, e: ft.ControlEvent, email_list: List[Dict]) -> None:
        content = self._get_email_modal_content()

        def save_item(e: ft.ControlEvent):
            new_email = content.content.value.strip()
            self._handle_save_email(dialog, e, new_email, email_list)
        
        dialog = self._create_dialog(
            title="Cadastrar Email",
            content=content,
            actions=[
                ft.CupertinoDialogAction("Salvar", on_click=save_item),
                ft.CupertinoDialogAction("Cancelar", on_click=lambda e: self.dialog_manager.dismiss_dialog(dialog, e)),
            ]
        )
        self.dialog_manager.show_dialog(dialog)
    
    def open_edit_modal(self, e: ft.ControlEvent, item: Dict) -> None:
        self.selected_item = item
        content = self._get_email_modal_content(item["email"])
        
        def save_item(e: ft.ControlEvent):
            new_email = content.content.value.strip()
            self._handle_save_email(dialog, e, new_email, [], is_edit=True)
        
        dialog = self._create_dialog(
            title="Editar Email",
            content=content,
            actions=[
                ft.CupertinoDialogAction("Salvar", on_click=save_item),
                ft.CupertinoDialogAction("Cancelar", on_click=lambda e: self.dialog_manager.dismiss_dialog(dialog, e)),
            ]
        )
        self.dialog_manager.show_dialog(dialog)
    
    def open_delete_modal(self, e: ft.ControlEvent, item: Dict, email_list: List[Dict]) -> None:
        self.selected_item = item
        
        def delete_email(e: ft.ControlEvent):
            if self.selected_item:
                email_list[:] = [item for item in email_list if item['id'] != self.selected_item['id']]
            self.dialog_manager.dismiss_dialog(dialog, e)
            self.refresh_callback()
        
        dialog = self._create_dialog(
            title="Deletar Email",
            content=ft.Text(
                spans=[
                    ft.TextSpan(text="Você tem certeza que deseja deletar o email "),
                    ft.TextSpan(text=item['email'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ft.TextSpan(text="?")
                ]
            ),
            actions=[
                ft.CupertinoDialogAction(
                    "OK", is_destructive_action=True, on_click=delete_email
                ),
                ft.CupertinoDialogAction(text="Cancel", on_click=lambda e: self.dialog_manager.dismiss_dialog(dialog, e)),
            ]
        )
        self.dialog_manager.show_dialog(dialog)