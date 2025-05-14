from data_access import UpdateExcelList

class SendBaseEmailsManager:
    def __init__(self):
        pass
    def run(self):
        updateList = UpdateExcelList(r'C:\Dev\Scripts\Python\python-tools\excel\PCO_Gestores.xlsx')
        updateList.updateList()