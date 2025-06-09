from typing import Optional
import flet as ft

from feature.components.handlers import EmailDialogHandler

class PcoListEmails(ft.Column):
    def __init__(self, email_list: list, email_dialog_handler: EmailDialogHandler, refresh_list, page: Optional[ft.Page] = None):
        super().__init__()
        self.current_page = 1
        self.items_per_page = 10
        self.email_list = email_list
        self.email_dialog_handler = email_dialog_handler
        self.page = page
        self.refresh_list = refresh_list
    
    def change_page(self, new_page):
        self.current_page = new_page
        self.refresh_list()

    def render_list(self) -> ft.Container:
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        paginated_items = self.email_list[start_index:end_index]

        tiles = []
        for item in paginated_items:
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
        
        total_pages = max(1, (len(self.email_list) + self.items_per_page - 1) // self.items_per_page)

        pagination_controls = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: self.change_page(self.current_page - 1),
                    disabled=self.current_page == 1
                ),
                ft.Text(f"Página {self.current_page} de {total_pages}"),
                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.change_page(self.current_page + 1),
                    disabled=self.current_page == total_pages
                ),
            ],
            spacing=20
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Column(controls=tiles, scroll=ft.ScrollMode.ALWAYS),
                    pagination_controls
                ]
            )
        )
