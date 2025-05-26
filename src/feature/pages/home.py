from collections import defaultdict
import json
import os
from datetime import datetime, timedelta
import flet as ft

class HomePage(ft.Column):
    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir
        self.data_file_history = os.path.join(self.data_dir, "emails_history.json")
        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.history_data = None
        self.expand = True
        self.spacing = 20

    def load_history(self) -> list:
        try:
            if os.path.exists(self.data_file_history):
                with open(self.data_file_history, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar emails: {e}")
        return []

    def _process_data(self) -> tuple:
        """Processa os dados para os últimos 15 dias e mensal"""
        daily_counts = defaultdict(int)
        monthly_counts = defaultdict(int)
        
        for entry in self.history_data:
            try:
                date_str = entry["timestamp"].split("T")[0]
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                month_key = date.strftime("%Y-%m")
                daily_counts[date] += entry.get("total_emails", 0)
                monthly_counts[month_key] += entry.get("total_emails", 0)
            except (KeyError, ValueError) as e:
                print(f"Erro ao processar entrada: {e}")
                continue
        
        # Processar últimos 15 dias
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=14)
        
        last15_dates = []
        last15_counts = []
        
        current_date = start_date
        while current_date <= end_date:
            last15_dates.append(current_date)
            last15_counts.append(daily_counts.get(current_date, 0))
            current_date += timedelta(days=1)
        
        # Processar dados mensais (últimos 6 meses)
        months = sorted(monthly_counts.keys(), reverse=True)[:6]
        month_labels = [datetime.strptime(m, "%Y-%m").strftime("%b/%Y") for m in months]
        month_counts = [monthly_counts[m] for m in months]
        
        return (last15_dates, last15_counts, month_labels, month_counts)

    def _create_summary_cards(self, total_15days: int, total_month: int) -> ft.Row:
        """Cria os cards de resumo"""
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
        """Cria um gráfico de barras"""
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

    def build(self):
        self.history_data = self.load_history()
        
        if not self.history_data:
            self.controls = [ft.Text("Nenhum dado histórico disponível", size=20)]
            return self
        
        # Processar dados
        last15_dates, last15_counts, month_labels, month_counts = self._process_data()
        total_15days = sum(last15_counts)
        total_month = sum(month_counts[:1])
        
        # Converter datas para formato de string (DD/MM)
        last15_labels = [d.strftime("%d/%m") for d in last15_dates]
        
        # Criar layout
        self.controls = [
            ft.Text("Dashboard de E-mails", size=24, weight="bold"),
            self._create_summary_cards(total_15days, total_month),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Últimos 15 dias", size=16, weight="bold"),
                            ft.Container(
                                self._create_chart(last15_labels, last15_counts, "Últimos 15 dias"),
                                height=300,
                                expand=True,
                            ),
                        ],
                        expand=True,
                    ),
                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                    ft.Column(
                        controls=[
                            ft.Text("Últimos 6 meses", size=16, weight="bold"),
                            ft.Container(
                                self._create_chart(month_labels, month_counts, "Últimos 6 meses", is_monthly=True),
                                height=300,
                                expand=True,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                spacing=20,
                expand=True,
            ),
        ]
        
        return self