import threading
import flet as ft
from typing import Optional

from feature.components.handlers import EmailDialogHandler
from feature.components.managers import DialogManager, NotificationManager
from feature.components.repositories import EmailRepository

class PcoReport(ft.Column):
    def __init__(self, notification: NotificationManager, page: Optional[ft.Page] = None, data_dir: str = ''):
        super().__init__()
        self.page = page
        self.current_page = 1
        self.items_per_page = 10
        self.notification = notification

        self.repo = EmailRepository(data_dir, self.notification)
        self.email_list = self.repo.load_emails()
        self.loading_indicator = ft.ProgressRing(
            visible=False,
            width=50,
            height=50,
            stroke_width=5
        )
        
        self.dialog_manager = DialogManager(page)
        self.notification_manager = NotificationManager(page)
        self.email_dialog_handler = EmailDialogHandler(
            page,
            dialog_manager=self.dialog_manager,
            notification_manager=self.notification_manager,
            refresh_callback=self.refresh_list_and_save
        )
    
    def refresh_list_and_save(self) -> None:
        """Updates the list and saves it to the JSON file"""
        self.repo.save_emails(self.email_list)
        self.refresh_list()
    
    def refresh_list(self) -> None:
        self.controls.clear()
        self.build()
        self.page.update()
    
    def change_page(self, new_page):
        self.current_page = new_page
        self.refresh_list()
    
    def send_report_with_loading(self, e):
        self.loading_indicator.visible = True
        self.page.update()
        emails = []
        for item in self.email_list:
            emails.append(item['email'])
        
        def task():
            try:
                self.repo.generate_report(emails)
            except Exception as err:
                print(f"Erro ao enviar relatório: {err}")
            finally:
                self.loading_indicator.visible = False
                self.page.update()
                
        threading.Thread(target=task, daemon=True).start()
        
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
                            ft.Icons.MAIL_SHARP,
                            icon_size=25,
                            tooltip='Enviar Relatório',
                            on_click=self.send_report_with_loading
                        ),
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE,
                            icon_size=25,
                            tooltip='Adicionar Email',
                            on_click=lambda e: self.email_dialog_handler.open_add_modal(e, self.email_list)
                        ),
                    ]
                ),
                content=ft.Column(
                    controls=[
                        self.render_list(),
                        ft.Row(
                            controls=[self.loading_indicator],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            )
        )
