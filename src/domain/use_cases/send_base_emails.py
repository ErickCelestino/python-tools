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

    def run(self):
        #self.update_lists()
        self.read_bases()
