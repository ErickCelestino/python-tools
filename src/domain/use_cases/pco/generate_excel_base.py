import logging
from typing import Any
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateExcelBase:
    def __init__(self, list_to_update: list[dict[str, Any]]):
        self.list_to_update = list_to_update
    
    def read_bases(self):
        for row in self.list_to_update:
            logger.info(f"Coletando dados da planilha: {row['path']}")
            if(row['id'] == 1):
                self.managers_list = pd.read_excel(row['path'])
            elif(row['id'] == 2):
                self.budget_sets = pd.read_excel(row['path'])
            elif(row['id'] == 3):
                self.references = pd.read_excel(row['path'])
    
    def transform_base(self):
        columns = ['ID', 'ID_Gerencia', 'ID_Gestor', 'Email_VP', 'Email_Gestor', 'Email_Regional', 'Gerente_Financeiro', 'Diretor_Financeiro', 'Marca', 'Filial', 'Conta', 'Verba', 'Centro_De_Custo', 'BU', 'CD_Planilha', 'VP', 'Descricao_VP', 'Grupo', 'Email', 'Email_Ferias', 'Data_Retorno_Ferias', 'De_Ferias']
        
        df_complete_base = self.references.merge(self.managers_list, left_on='ID_Gestor', right_on='ID', suffixes=('', '_managers'))
        df_complete_base = df_complete_base.merge(self.budget_sets, left_on='ID_Gerencia', right_on='ID', suffixes=('', '_sets'))
        
        df_complete_base = df_complete_base[columns]
        df_complete_base['De_Ferias'] = df_complete_base['De_Ferias'].map({True: 'Sim', False: 'Não'})
        df_complete_base = df_complete_base.rename(columns={'ID_Gerencia': 'ID_Conjunto'})
        
        df_complete_base.to_excel("Acessos_PCO_Base_Completa.xlsx", index=False)
    
    def run(self):
        self.read_bases()
        self.transform_base()
