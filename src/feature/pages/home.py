from collections import defaultdict
import json
import os
from datetime import datetime, timedelta
import flet as ft

from feature.components.handlers import HomeChartHandler

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
        self.chart_handler = HomeChartHandler()

    def load_history(self) -> list:
        try:
            if os.path.exists(self.data_file_history):
                with open(self.data_file_history, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar emails: {e}")
        return []

    def _process_data(self) -> tuple:
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
        
        # Process last 15 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=14)
        
        last15_dates = []
        last15_counts = []
        
        current_date = start_date
        while current_date <= end_date:
            last15_dates.append(current_date)
            last15_counts.append(daily_counts.get(current_date, 0))
            current_date += timedelta(days=1)
        
        # process data month (last 6 months)
        months = sorted(monthly_counts.keys(), reverse=True)[:6]
        month_labels = [datetime.strptime(m, "%Y-%m").strftime("%b/%Y") for m in months]
        month_counts = [monthly_counts[m] for m in months]
        
        return (last15_dates, last15_counts, month_labels, month_counts)

    def build(self):
        self.history_data = self.load_history()
        
        if not self.history_data:
            self.controls = [ft.Text("Nenhum dado histórico disponível", size=20)]
            return self
        
        # Process data
        last15_dates, last15_counts, month_labels, month_counts = self._process_data()
        total_15days = sum(last15_counts)
        total_month = sum(month_counts[:1])
        
        # Convert dates for string format (DD/MM)
        last15_labels = [d.strftime("%d/%m") for d in last15_dates]
        
        # Create layout
        self.controls = [
            ft.Text("Dashboard de E-mails", size=24, weight="bold"),
            self.chart_handler._create_summary_cards(total_15days, total_month),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Últimos 15 dias", size=16, weight="bold"),
                            ft.Container(
                                self.chart_handler._create_chart(last15_labels, last15_counts, "Últimos 15 dias"),
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
                                self.chart_handler._create_chart(month_labels, month_counts, "Últimos 6 meses", is_monthly=True),
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