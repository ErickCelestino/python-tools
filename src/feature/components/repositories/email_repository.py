import json
import os
from pathlib import Path

class EmailRepository:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
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