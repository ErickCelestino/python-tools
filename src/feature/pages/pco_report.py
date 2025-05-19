import flet as ft
from typing import Optional

from feature.components.handlers import EmailDialogHandler
from feature.components.managers import DialogManager

list_test = [
    {
        'id': '1',
        'created_at': '26/04/2025',
        'email': 'erickcelestimo@gmail.com'
    }
]
class PcoReport(ft.Column):
    def __init__(self, page: Optional[ft.Page] = None):
        super().__init__()
        self.page = page
        self.email_list = list_test.copy()
        
        self.dialog_manager = DialogManager(page)
        self.email_dialog_handler = EmailDialogHandler(
            dialog_manager=self.dialog_manager,
            refresh_callback=self.refresh_list
        )
    
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