import logging
from typing import Any
from data_access import UpdateExcelList

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateBaseManager:
    def __init__(self, list_to_update: list[dict[str, Any]]):
        self.list_to_update = list_to_update
    
    def update_lists(self):
        for row in self.list_to_update:
            logger.info(f"Acessando a planilha: {row['path']}")
            updateList = UpdateExcelList(row['path'])
            updateList.updateList()

    def run(self):
        self.update_lists()
