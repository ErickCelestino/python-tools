from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[4]

class PcoCheckReferences:
    def __init__(self, notify_callback=None):
        self.budget_set_path =  str(project_root / 'excel' / 'PCO_Conjuntos.xlsx')
        self.manager_path = str(project_root / 'excel' / 'PCO_Gestores.xlsx')
        self.references_path = str(project_root / 'excel' / 'PCO_Referencias.xlsx')
        self.not_found = []
        self.notify_callback = notify_callback or (lambda msg, bgcolor='': None)
    
    def _notify(self, message: str, bgcolor='green', text_color='white'):
        self.notify_callback(message, bgcolor, text_color)
    
    def _verifiedDataById(self, value_id, data: pd.DataFrame):
        return data[data['ID'] == value_id]
    
    def _add_not_found(self, verified_data, data_ids):
        if verified_data.empty:
            self.not_found.append({
                'ID': data_ids['id_reference'],
                'ID_Gestor': data_ids['id_manager'],
                'ID_Gerencia': data_ids['id_budget_set'],
            })
    
    def read_excel(self):
        self.budget_set = pd.read_excel(self.budget_set_path)
        self.manager = pd.read_excel(self.manager_path)
        self.references = pd.read_excel(self.references_path)
    
    def create_not_found_references_file(self):
        if len(self.not_found) > 0:
            pd.DataFrame(self.not_found).to_excel("referencias_nao_encontradas.xlsx", index=False)
            
    def check_references(self):
        self._notify("⚠️ Verificação Iniciada", bgcolor='yellow', text_color='black')
        for i, row, in enumerate(self.references.itertuples(index=False)):
            group_row = row._asdict()
            data_ids = {
                'id_reference': group_row.get('ID'),
                'id_manager': group_row.get('ID_Gestor'),
                'id_budget_set': group_row.get('ID_Gerencia')
            }
            
            verifiedManager = self._verifiedDataById(data_ids['id_manager'], self.manager)
            varifiedBudgetSet = self._verifiedDataById(data_ids['id_budget_set'], self.budget_set)
    
            self._add_not_found(verifiedManager, data_ids)
            self._add_not_found(varifiedBudgetSet, data_ids)
            
    def run(self):
        self.read_excel()
        self.check_references()
        self.create_not_found_references_file()
        self._notify("✅ Verificação Completa", bgcolor='green')