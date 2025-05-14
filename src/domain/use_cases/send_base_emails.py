from data_access import UpdateExcelList

class SendBaseEmailsManager:
    def __init__(self):
        self.list_to_update = [
            r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Gestores.xlsx',
            r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Conjuntos.xlsx',
            r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Referencias.xlsx'
        ]
    
    def update_lists(self):
        for row in self.list_to_update:
            print(f'Acessando a planilha: {row}')
            updateList = UpdateExcelList(row)
            updateList.updateList()

    def run(self):
        self.update_lists()
