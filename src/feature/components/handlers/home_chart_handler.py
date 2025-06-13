import flet as ft

class HomeChartHandler:
    def __init__(self):
        pass
    
    def _create_summary_cards(self, total_15days: int, total_month: int) -> ft.Row:
        """Create resume cards"""
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Total últimos 15 dias", size=14),
                            ft.Text(str(total_15days), size=24, weight="bold"),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE,
                    width=200,
                    height=100,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Total este mês", size=14),
                            ft.Text(str(total_month), size=24, weight="bold"),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.Colors.GREEN,         
                    width=200,
                    height=100,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _create_chart(self, labels, values, title, is_monthly=False) -> ft.BarChart:
        """Create one bar graph"""
        max_value = max(values) if values else 1
        
        return ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=value,
                            width=20 if not is_monthly else 30,
                            color=ft.Colors.BLUE if not is_monthly else ft.Colors.GREEN,
                            tooltip=f"{label}: {value} email{'s' if value != 1 else ''}",
                            border_radius=4,
                        ),
                    ],
                )
                for idx, (label, value) in enumerate(zip(labels, values))
            ],
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Disparos"),
                title_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=idx,
                        label=ft.Text(label.split("/")[0] if is_monthly else label),
                    )
                    for idx, label in enumerate(labels)
                    if idx % (2 if not is_monthly else 1) == 0
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
            interactive=True,
            expand=True,
            max_y=max_value + (5 - max_value % 5) if max_value % 5 != 0 else max_value + 5,
        )