import win32com.client

class UpdateExcelList:
    def __init__(self, excel_path):
        self.excel_path = excel_path
    
    def updateList(self):
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False

        workbook = excel.Workbooks.Open(self.excel_path)
        workbook.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        workbook.Save()
        workbook.Close(False)
        excel.Quit()