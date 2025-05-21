import json
import os
import flet as ft

class HomePage(ft.Column):
    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir
        self.data_file_history = os.path.join(self.data_dir, "emails_history.json")
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.hotory_data = None
    
    def load_hitory(self) -> list:
        try:
            if os.path.exists(self.data_file_history):
                with open(self.data_file_history, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar emails: {e}")
        return []

    def build(self):
        self.hotory_data = self.load_hitory()
        print(self.hotory_data)
        text = ft.ElevatedButton(text='nome', width=200)
        self.controls.append(text)

