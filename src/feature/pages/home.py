import flet as ft

class HomePage(ft.Column):
    def __init__(self):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def build(self):
        print('Passou na Home')
        text = ft.ElevatedButton(text='nome', width=200)
        self.controls.append(text)
        # nomes_botoes = ["Início", "Relatório PCO", "Sair"]
        
        # for nome in nomes_botoes:
        #     btn = ft.ElevatedButton(text=nome, on_click=self.on_click, width=200)
        #     self.controls.append(btn)
