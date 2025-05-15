import os
import sys
from PIL import Image

from .tray_icon_frame import TrayIconFrame

class PyInstallerFrame:
    def __init__(self, page, icon_path):
        self.page = page
        self.icon_path = icon_path
        self.tray_manager = None

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def setup_tray_icon(self):
        icon = Image.open(self.icon_path)
        self.tray_manager = TrayIconFrame(
            window=self.page,
            tooltip="Encaminhador de E-mails",
            icon_image=icon,
            menu_items=[]
        )