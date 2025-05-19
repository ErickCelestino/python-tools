import flet as ft

list_test = [
    {
        'id': '1',
        'created_at': '26/04/2025',
        'email': 'erickcelestimo@gmail.com'
    }
]

class PcoReport(ft.Column):
    def __init__(self, page=None):
        super().__init__()
        self.page = page  # Armazena a referência à página
        self.dlg_modal = None
        self.delete_dlg = None 
        self.selected_item = None 
    
    def _redirect(self, e):
        print('Ação')
    
    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def close_delete_dlg(self, e):
        self.delete_dlg.open = False
        self.page.update()
    
    def open_dlg_modal(self, e, item=None):
        self.selected_item = item
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Email"),
            content=ft.TextField(
                value=item["email"] if item else "",
                label="Email",
                autofocus=True
            ),
            actions=[
                ft.TextButton("Salvar", on_click=self.save_item),
                ft.TextButton("Cancelar", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_modal  # Corrigido typo: dialog -> dialog
        self.dlg_modal.open = True
        self.page.update()

    def save_item(self, e):
        new_email = self.dlg_modal.content.value
        if self.selected_item:
            self.selected_item["email"] = new_email
        self.close_dlg(e)
        # Atualiza a lista de forma mais eficiente
        self.controls[0].content.controls = self.render_list().content.controls
        self.page.update()

    def open_delete_dialog(self, e, item):
        self.selected_item = item
        self.delete_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o email {item['email']}?"),
            actions=[
                ft.TextButton("Sim", on_click=self.delete_item),
                ft.TextButton("Não", on_click=self.close_delete_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.delete_dlg
        self.delete_dlg.open = True
        self.page.update()
    
    def delete_item(self, e):
        if self.selected_item:
            # Remove o item da lista
            list_test[:] = [item for item in list_test if item['id'] != self.selected_item['id']]
        self.close_delete_dlg(e)
        # Atualiza a lista de forma mais eficiente
        self.controls[0].content.controls = self.render_list().content.controls
        self.page.update()

    def render_list(self):
        tiles = []
        for item in list_test:
            tile = ft.CupertinoListTile(
                additional_info=ft.Text(item['created_at']),
                bgcolor_activated=ft.Colors.AMBER_ACCENT,
                leading=ft.Icon(name=ft.CupertinoIcons.MAIL),
                title=ft.Text(item['email']),
                trailing=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="blue",
                            tooltip="Editar",
                            on_click=lambda e, item=item: self.open_dlg_modal(e, item)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            tooltip="Excluir",
                            on_click=lambda e, item=item: self.open_delete_dialog(e, item)
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.END,
                )
            )
            tiles.append(tile)

        return ft.Container(content=ft.Column(controls=tiles))

    def build(self):
        self.controls.append(
            ft.Pagelet(
                appbar=ft.AppBar(
                    leading=ft.Icon(ft.Icons.DOCUMENT_SCANNER),
                    leading_width=40,
                    title=ft.Text("PCO Relatório"),
                    center_title=False,
                    actions=[
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE,
                            on_click=self._redirect
                        ),
                    ]
                ),
                content=self.render_list(),
            )
        )
        return self