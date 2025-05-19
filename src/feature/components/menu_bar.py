import flet as ft

class MenuBar(ft.Column):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.alignment = ft.MainAxisAlignment.START
        self.selected_index = 0

    def build(self):
        self.options = [
            {
                'title': 'Início',
                'route': 'home',
                'icon': ft.Icons.HOME_OUTLINED,
                'icon_selected': ft.Icons.HOME
            },
            {
                'title': 'Relatorio PCO',
                'route': 'report_pco',
                'icon': ft.Icons.DOCUMENT_SCANNER_OUTLINED,
                'icon_selected': ft.Icons.DOCUMENT_SCANNER
            }
        ]

        self.drawer = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            min_extended_width=400,
            group_alignment=0.9,
            height=120,
            destinations=[
                ft.NavigationRailDestination(
                    icon=option['icon'],
                    selected_icon=option['icon_selected'],
                    label=option['title'],
                ) for option in self.options
            ],
            on_change=self._on_destination_selected
        )
            
        self.controls.append(self.drawer)

    def _on_destination_selected(self, e):
        index = e.control.selected_index
        selected_route = self.options[index]["route"]
        self.on_navigate(selected_route)