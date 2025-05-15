import flet as ft
from dotenv import load_dotenv
from app import App
from feature.pages import HomePage

def main(page: ft.Page):
    load_dotenv()
    page.title = 'Vitru dev Tools'
    page.window.maximized = True
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START

    app = App(page)
    page.add(app)

ft.app(target=main)

# if __name__ == "__main__":
#     main()
# SendBaseEmailsManager(
#         ['erick.celestino@vitru.com.br'],
#         'Acessos_PCO_Base_Completa.xlsx',
#         'Relatório PCO Base Completa',
#         'Olá,\n\nEste é um e-mail enviado automaticamente via Outlook.\n\nAtt,\nVP Finanças',
#     )