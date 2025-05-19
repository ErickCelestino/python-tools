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
        self.page = page
        self.selected_item = None
        self.email_list = list_test
    
    def open_add_modal(self, e):
        def dismiss_dialog(e):
            cupertino_alert_dialog.open = False
            e.control.page.update()

        def save_item(e):
            text_field = cupertino_alert_dialog.content.content
            new_email = text_field.value
            print(new_email)
            if self.selected_item:
                self.selected_item["email"] = new_email
            dismiss_dialog(e)
            self.refresh_list()
    
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Cadastrar Email"),
            content=ft.Container(
                ft.TextField(
                    label="Email",
                    autofocus=True
                ),
                height=80,
                alignment=ft.alignment.center,
            ),
            actions=[
                ft.CupertinoDialogAction("Salvar", on_click=save_item),
                ft.CupertinoDialogAction("Cancelar", on_click=dismiss_dialog),
            ],
        )
    
        e.control.page.overlay.append(cupertino_alert_dialog)
        cupertino_alert_dialog.open = True
        e.control.page.update()
    
    def open_edit_modal(self, e, item):
        self.selected_item = item
        def dismiss_dialog(e):
            cupertino_alert_dialog.open = False
            e.control.page.update()

        def save_item(e):
            text_field = cupertino_alert_dialog.content.content
            new_email = text_field.value
            print(new_email)
            if self.selected_item:
                self.selected_item["email"] = new_email
            dismiss_dialog(e)
            self.refresh_list()

        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Editar Email"),
            content=ft.Container(
                ft.TextField(
                    value=item["email"],
                    label="Email",
                    autofocus=True
                ),
                height=80,
                alignment=ft.alignment.center,
            ),
            actions=[
                ft.CupertinoDialogAction("Salvar", on_click=save_item),
                ft.CupertinoDialogAction("Cancelar", on_click=dismiss_dialog),
            ],
        )

        e.control.page.overlay.append(cupertino_alert_dialog)
        cupertino_alert_dialog.open = True
        e.control.page.update()

    def open_delete_modal(self, e, item):
        self.selected_item = item

        def dismiss_dialog(e):
            cupertino_alert_dialog.open = False
            e.control.page.update()

        def delete_email(e):
            if self.selected_item:
                self.email_list[:] = [item for item in self.email_list if item['id'] != self.selected_item['id']]
            cupertino_alert_dialog.open = False
            self.refresh_list()
            e.control.page.update()
    
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Deletar Email"),
            content=ft.Text(
                spans=[
                    ft.TextSpan(text="Você tem certeza que deseja deletar o email "),
                    ft.TextSpan(text=item['email'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ft.TextSpan(text="?")
                ]
            ),
            actions=[
                ft.CupertinoDialogAction(
                    "OK", is_destructive_action=True, on_click=delete_email
                ),
                ft.CupertinoDialogAction(text="Cancel", on_click=dismiss_dialog),
            ],
        )
        e.control.page.overlay.append(cupertino_alert_dialog)
        cupertino_alert_dialog.open = True
        e.control.page.update()

    def refresh_list(self):
        self.controls.clear()
        self.build()
        self.page.update()

    def render_list(self):
        tiles = []
        for item in self.email_list:
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
                            on_click=lambda e, item=item: self.open_edit_modal(e, item)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            tooltip="Excluir",
                            on_click=lambda e, item=item: self.open_delete_modal(e, item)
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
                            on_click=self.open_add_modal
                        ),
                    ]
                ),
                content=self.render_list()
            )
        )