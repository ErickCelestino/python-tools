import flet as ft

class HomePage(ft.Column):
    def __init__(self):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.build()

    def on_click(self, e):
        dlg = ft.AlertDialog(title=ft.Text(f"Você clicou em: {e.control.text}"))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def build(self):
        nomes_botoes = ["Início", "Perfil", "Configurações", "Sair"]
        
        for nome in nomes_botoes:
            btn = ft.ElevatedButton(text=nome, on_click=self.on_click, width=200)
            self.controls.append(btn)
