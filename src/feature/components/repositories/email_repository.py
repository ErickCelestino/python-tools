import json
import os
from pathlib import Path
from typing import Dict, List

from domain.use_cases import SendBaseEmailsManager
from feature.components.managers import NotificationManager

class EmailRepository:
    def __init__(self, data_dir: str, notify_callback: NotificationManager):
        self.data_dir = data_dir
        self.notify_callback = notify_callback
        self.data_file = os.path.join(self.data_dir, "emails.json")
        self.ensure_data_dir_exists()

    def ensure_data_dir_exists(self):
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def load_emails(self) -> list:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar emails: {e}")
        return []

    def save_emails(self, email_list: list) -> None:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(email_list, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Erro ao salvar emails: {e}")

    def generate_report(self, email_list: List[Dict]):
        self.notify_callback.show_notification('Iniciando Processo de Envio', 'yellow', 'black')
        SendBaseEmailsManager(
            email_list,
            'Acessos_PCO_Base_Completa.xlsx',
            'Relatório PCO Base Completa',
            'Olá,\n\nEste é um e-mail enviado automaticamente via Outlook.\n\nAtt,\nVP Finanças',
            self.notify_callback.show_notification
        ).run()