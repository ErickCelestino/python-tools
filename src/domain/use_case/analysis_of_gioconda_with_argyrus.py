import pandas as pd

class AnalysisOfGiocondaWithArgyrus:
    def __init__(self):
        self.df_gioconda = None
        self.df_argyrus = None
    
    def convert_excel_to_csv(self):
        df_argyrus_sheets = pd.read_excel(
            r'C:\Dev\Python\python-tools\excel\bases\Cobranca_Em_Aberto_Argyrus.xlsx',
            sheet_name=None
        )
        
        self.df_argyrus = pd.concat(
            [df.assign(origem=nome) for nome, df in df_argyrus_sheets.items()],
            ignore_index=True
        )
        
        self.df_argyrus['COBRANCA'] = self.df_argyrus['COBRANCA'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')
    
    def read_bases(self):
        self.df_gioconda = pd.read_csv(
            r'C:\Dev\Python\python-tools\excel\bases\cobrancas_alunos.csv',
            sep=';',
            encoding='latin1'
        )
        
        self.df_argyrus = pd.read_csv(
            r'C:\Dev\Python\python-tools\excel\bases\2024_2025\cobranca_em_aberto_argyrus.csv',
            sep=';',
            encoding='utf-8'
        )
    
    def titles_with_exists_in_gioconda_and_exists_in_argyrus(self):
        df =  self.df_argyrus[~self.df_argyrus['COBRANCA'].isin(self.df_gioconda['COBRANCA'])]
        print(len(df))
        #df.to_excel(r'C:\Dev\Python\python-tools\excel\results\relatorio_consta_argyrus_nao_consta_gioconda.xlsx', index=False)
    
    def run(self):
        self.read_bases()
        self.titles_with_exists_in_gioconda_and_exists_in_argyrus()