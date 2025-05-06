import pandas as pd
from data_access import TransformColumnsInLines

class SendBaseEmailsManager:
    def __init__(self):
        self.dataFrame = pd.read_excel('teste.xlsx')
        self.resultFilePath = 'tabela_referencia.xlsx'
        self.fixedColumns = ['Descricao VP', 'VP', 'BU', 'CD_Planilha', 'Verba', 'Centro de Custo', 'Conta', 'Filial', 'Marca', 'Gerente Financeiro', 'Diretor Financeiro', 'E-mail Regional', 'E-mail Gestor', 'E-mail VP']

    def run(self):
        TransformColumnsInLines(self.dataFrame, self.fixedColumns, self.resultFilePath).transform()