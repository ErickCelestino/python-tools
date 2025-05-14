from domain import SendBaseEmailsManager
from dotenv import load_dotenv

def main():
    load_dotenv()
    renderDashboard = SendBaseEmailsManager(
        ['erick.celestino@vitru.com.br'],
        'Acessos_PCO_Base_Completa.xlsx',
        'Relatório PCO Base Completa',
        'Olá,\n\nEste é um e-mail enviado automaticamente via Outlook.\n\nAtt,\nVP Finanças',
    )
    renderDashboard.run()

if __name__ == "__main__":
    main()