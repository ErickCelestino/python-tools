import json
import flet as ft
from typing import Optional
import os
from pathlib import Path

from feature.components.handlers import EmailDialogHandler
from feature.components.managers import DialogManager

class PcoReport(ft.Column):
    def __init__(self, page: Optional[ft.Page] = None, data_dir = ''):
        super().__init__()
        self.page = page
        self.data_dir = data_dir
        self.data_file = os.path.join(self.data_dir, "emails.json")
        self.email_list = self.load_emails()
        
        self.dialog_manager = DialogManager(page)
        self.email_dialog_handler = EmailDialogHandler(
            dialog_manager=self.dialog_manager,
            refresh_callback=self.refresh_list_and_save
        )
    
    def ensure_data_dir_exists(self):
        """Ensures the data directory exists"""
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def load_emails(self) -> list:
        """Loads emails from JSON file or returns empty list if none exists"""
        try:
            self.ensure_data_dir_exists() 
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar emails: {e}")

        return []
    
    def refresh_list_and_save(self) -> None:
        """Updates the list and saves it to the JSON file"""
        self.save_emails()
        self.refresh_list()
    
    def save_emails(self) -> None:
        """Saves email list to JSON file, creating folder if necessary"""
        try:
            self.ensure_data_dir_exists() 
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.email_list, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Erro ao salvar emails: {e}")
    
    def refresh_list(self) -> None:
        self.controls.clear()
        self.build()
        self.page.update()
    
    def render_list(self) -> ft.Container:
        tiles = []
        for item in self.email_list:
            tile = ft.CupertinoListTile(
                additional_info=ft.Text(item['created_at']),
                bgcolor_activated=ft.Colors.AMBER_ACCENT,
                leading=ft.Icon(name=ft.CupertinoIcons.MAIL),
                title=ft.Text(item['email']),
                trailing=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="blue",
                            tooltip="Editar",
                            on_click=lambda e, item=item: self.email_dialog_handler.open_edit_modal(e, item)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            tooltip="Excluir",
                            on_click=lambda e, item=item: self.email_dialog_handler.open_delete_modal(e, item, self.email_list)
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.END,
                )
            )
            tiles.append(tile)

        return ft.Container(content=ft.Column(controls=tiles))
    
    def build(self) -> None:
        self.controls.append(
            ft.Pagelet(
                appbar=ft.AppBar(
                    leading=ft.Icon(ft.Icons.DOCUMENT_SCANNER),
                    leading_width=40,
                    title=ft.Text("PCO Relatório"),
                    center_title=False,
                    actions=[
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE,
                            on_click=lambda e: self.email_dialog_handler.open_add_modal(e, self.email_list)
                        ),
                    ]
                ),
                content=self.render_list()
            )
        )