import pandas as pd
from data_access import UpdateExcelList

class SendBaseEmailsManager:
    def __init__(self):
        self.list_to_update = [
            {
                'id': 1,
                'path': r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Gestores.xlsx'
            },
            {
                'id': 2,
                'path': r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Conjuntos.xlsx'
            },
            {
                'id': 3,
                'path': r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Referencias.xlsx'
            }
        ]
    
    def update_lists(self):
        for row in self.list_to_update:
            print(f'Acessando a planilha: {row['path']}')
            updateList = UpdateExcelList(row['path'])
            updateList.updateList()

    def read_bases(self):
        for row in self.list_to_update:
            if(row['id'] == 1):
                print(f'Coletando dados da planilha: {row['path']}')
                self.managers_list = pd.read_excel(row['path'])
            elif(row['id'] == 2):
                print(f'Coletando dados da planilha: {row['path']}')
                self.budget_sets = pd.read_excel(row['path'])
            elif(row['id'] == 3):
                print(f'Coletando dados da planilha: {row['path']}')
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
        self.update_lists()
        self.read_bases()
        self.transform_base()
