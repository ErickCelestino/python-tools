import flet as ft
from typing import Optional

from feature.components import PcoDialogHandler, DialogManager, NotificationManager, EmailRepository, PcoAppBar,PcoListEmails

class PcoReport(ft.Column):
    def __init__(self, notification: NotificationManager, page: Optional[ft.Page] = None, data_dir: str = ''):
        super().__init__()
        self.page = page
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
        self.email_dialog_handler = PcoDialogHandler(
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

    def build(self) -> None:
        appBar = PcoAppBar(self.email_dialog_handler, self.repo, self.loading_indicator, self.email_list, self.page)
        emailsList = PcoListEmails(self.email_list, self.email_dialog_handler, self.refresh_list, self.page)
        self.controls.append(
            ft.Pagelet(
                appbar=appBar.build(),
                content=ft.Column(
                    controls=[
                        emailsList.render_list(),
                        ft.Row(
                            controls=[self.loading_indicator],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            )
        )
