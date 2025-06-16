import threading
from typing import Optional
import flet as ft

from feature.components.handlers import PcoDialogHandler
from feature.components.repositories import EmailRepository

class PcoAppBar(ft.Column):
    def __init__(self, pco_dialog_handler: PcoDialogHandler, repo: EmailRepository, loading_indicator: ft.ProgressRing, email_list: list, page: Optional[ft.Page] = None):
        super().__init__()
        self.pco_dialog_handler = pco_dialog_handler
        self.repo = repo
        self.loading_indicator = loading_indicator
        self.email_list = email_list
        self.page = page

    def _init_loading(self):
        self.loading_indicator.visible = True
        self.page.update()
        
    def __end_loading(self):
        self.loading_indicator.visible = False
        self.page.update()

    def send_report_with_loading(self, e):
        self._init_loading()
        emails = []
        for item in self.email_list:
            emails.append(item['email'])
        
        def task():
            try:
                self.repo.generate_report(emails)
            except Exception as err:
                print(f"Erro ao enviar relatório: {err}")
            finally:
                self.__end_loading()
                
        threading.Thread(target=task, daemon=True).start()

    def check_references(self):
        self._init_loading()
        self.pco_dialog_handler.open_check_references()
        self.__end_loading()
    
    def build(self):
        return ft.AppBar(
                leading=ft.Icon(ft.Icons.DOCUMENT_SCANNER),
                leading_width=40,
                title=ft.Text("PCO Relatório"),
                center_title=False,
                actions=[
                    ft.IconButton(
                        ft.Icons.CHECK_SHARP,
                        icon_size=25,
                        tooltip='Verificar Referencias',
                        on_click=lambda e: self.check_references()
                    ),
                    ft.IconButton(
                        ft.Icons.COMPARE_SHARP,
                        icon_size=25,
                        tooltip='Comparar Bases',
                        on_click=lambda e: self.pco_dialog_handler.open_compare_bases()
                    ),
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
                        on_click=lambda e: self.pco_dialog_handler.open_add_modal(e, self.email_list)
                    ),
                ]
            )