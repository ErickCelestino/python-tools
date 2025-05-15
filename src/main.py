import flet as ft
from dotenv import load_dotenv
from feature import HomePage


def main(page: ft.Page):
    load_dotenv()
    page.title = 'Teste'

    home = HomePage()
    page.add(home)

ft.app(main)

# if __name__ == "__main__":
#     main()
# SendBaseEmailsManager(
#         ['erick.celestino@vitru.com.br'],
#         'Acessos_PCO_Base_Completa.xlsx',
#         'Relatório PCO Base Completa',
#         'Olá,\n\nEste é um e-mail enviado automaticamente via Outlook.\n\nAtt,\nVP Finanças',
#     )