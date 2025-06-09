import pandas as pd

class TransformColumnsInLines:
    def __init__(self, dataFrame: pd.DataFrame, fixedColumns: list[str], excelPath: str):
        self.df = dataFrame
        self.fixedColumns = fixedColumns
        self.excelPath = excelPath

    def transform(self):
        columnsForMelt = [col for col in self.df.columns if col not in self.fixedColumns]

        df_melted = pd.melt(
            self.df,
            id_vars=self.fixedColumns,
            value_vars=columnsForMelt,
            var_name='Atributo',
            value_name='Valor'
        )
        
        df_melted = df_melted.dropna(subset=['Valor'])
        df_melted = df_melted[df_melted['Valor'].astype(str).str.strip() != ''] 
        df_melted.to_excel(self.excelPath, index=False)
