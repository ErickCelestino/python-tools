import sys
import pandas as pd
from pathlib import Path
import logging
import pythoncom

from domain.use_cases.pco import UpdateBaseManager
from feature.components.managers import NotificationManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parents[4]

class PcoBaseAnalysisManager:
    def __init__(self, excel_path: str, notify_callback: NotificationManager=None):
        self.excel_path = excel_path
        self.df = None
        self.notify_callback = notify_callback
        self.budget_set_path =  str(project_root / 'excel' / 'PCO_Conjuntos.xlsx')
        self.manager_path = str(project_root / 'excel' / 'PCO_Gestores.xlsx')
        self.references_path = str(project_root / 'excel' / 'PCO_Referencias.xlsx')
    
    def read_excel(self):
        self.df = pd.read_excel(self.excel_path)
        self.budget_set = pd.read_excel(self.budget_set_path)
        self.manager = pd.read_excel(self.manager_path)
        self.references = pd.read_excel(self.references_path)
    
    def notify(self, message: str, bgcolor='green', text_color='white'):
        self.notify_callback.show_notification(message, bgcolor, text_color)
        
    def save_bases(self, found: list, not_found = list):
        found = pd.DataFrame(found)
        not_found = pd.DataFrame(not_found)
        
        if(len(found) > 0):
            found.to_excel('referencias.xlsx', index=False, engine='openpyxl')

        if(len(not_found) > 0 ):
            not_found.to_excel('naoEncontrados.xlsx', index=False, engine='openpyxl')

        self.notify(f"Dados processados com sucesso!", bgcolor='green')
    
    def handle_bases(self):
        found = []
        not_found = []
        total_row = len(self.df)
        self.notify(f"Excel carregado com {total_row} linhas.", bgcolor='yellow', text_color='black')
        id_aux = int(self.references['ID_AUX'].iloc[-1]) + 1
        
        self.df.columns = [col.replace(' ', '_') for col in self.df.columns]
        for i, row, in enumerate(self.df.itertuples(index=False)):
            group_row = row._asdict()
            branch = group_row.get('Filial')
            account = group_row.get('Conta')
            verb = group_row.get('Verba')
            cost_center = group_row.get('Centro_de_Custo')
            bu = group_row.get('BU')
            cd_sheet = group_row.get('CD_Planilha')
            email = group_row['emails']
            
            verify_group = self.budget_set[(self.budget_set['Filial'] == branch) &
                                 (self.budget_set['Conta'] == account) &
                                 (self.budget_set['Verba'] == verb) &
                                 (self.budget_set['Centro_De_Custo'] == cost_center) &
                                 (self.budget_set['BU'] == bu) &
                                 (self.budget_set['CD_Planilha'] == cd_sheet)]
            
            verify_manager = self.manager[self.manager['Email'] == email]
            
            if not verify_group.empty and not verify_manager.empty:
                id_conjunto = verify_group.iloc[0]['ID']
                id_gestor = verify_manager.iloc[0]['ID']
                
                verificaReferencia = self.references[(self.references['ID_Gerencia'] == id_conjunto) &
                                                (self.references['ID_Gestor'] == id_gestor)]
                
                if verificaReferencia.empty:
                    nova_linha = {
                        'ID_Gerencia': id_conjunto,
                        'ID_Gestor': id_gestor,
                        'ID_AUX': id_aux
                    }
                    found.append(nova_linha)
                    
                    id_aux = id_aux + 1

            else:
                not_found.append({
                    'Filial': branch,
                    'Conta': account,
                    'Verba': verb,
                    'Centro_De_Custo': cost_center,
                    'BU': bu,
                    'CD_Planilha': cd_sheet,
                    'emails': email
                })
                sys.stdout.write(f"\rProcessados {i}/{total_row} clientes ({i/total_row:.1%})...\r")
                sys.stdout.flush()
                
        self.save_bases(found, not_found)
    
    def handle_references(self):
        colunas_fixas = ['Descricao VP', 'VP', 'BU', 'CD_Planilha', 'Verba', 'Centro de Custo', 'Conta', 'Filial', 'Marca', 'Gerente Financeiro', 'Diretor Financeiro', 'E-mail Regional', 'E-mail Gestor', 'E-mail VP']
        colunas_para_derreter = [col for col in self.df.columns if col not in colunas_fixas]
        df_melted = pd.melt(
            self.df,
            id_vars=colunas_fixas,
            value_vars=colunas_para_derreter,
            var_name='tipo_email',
            value_name='emails'
        )
        df_melted = df_melted[~df_melted['emails'].isna() & (df_melted['emails'].str.strip() != '')]
        df_melted = df_melted.drop_duplicates()
        self.df = df_melted
    
    def update_base(self):
        pythoncom.CoInitialize()
        try:
            UpdateBaseManager().run()
        finally:
            pythoncom.CoUninitialize()   
    
    def run(self):
        self.update_base()
        self.read_excel()
        self.handle_references()
        self.handle_bases()        