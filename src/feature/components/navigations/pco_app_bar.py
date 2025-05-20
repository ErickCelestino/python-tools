import threading
import flet as ft

from feature.components.handlers import EmailDialogHandler
from feature.components.repositories import EmailRepository

class PcoAppBar(ft.Column):
    def __init__(self, email_dialog_handler: EmailDialogHandler, repo: EmailRepository, loading_indicator: ft.ProgressRing, email_list: list):
        super().__init__()
        self.email_dialog_handler = email_dialog_handler
        self.repo = repo
        self.loading_indicator = loading_indicator
        self.email_list = email_list

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

    def build(self):
        return ft.AppBar(
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
            )