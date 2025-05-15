from tkinter import BooleanVar, Image, Tk, ttk
from .py_installer_frame import PyInstallerFrame


class HomeFrame:
    def __init__(self):
        self.tray_manager = None
        self.page = None
        self.icon_path = None
        self.py_manager = None

    def window_setup(self):
        self.page = Tk()
        self.startup_var = BooleanVar()
        self.page.title('Encaminhador de E-mails')
        self.page.geometry('600x600')
        self.page.resizable(False, False)

        tmp_manager = PyInstallerFrame(self.page, '')
        self.icon_path = tmp_manager.resource_path('assets/icon.ico')
        self.page.iconbitmap(self.icon_path)

        # Setting the style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 9))
        self.page.update_idletasks()

        # Gets the screen dimensions
        screen_width = self.page.winfo_screenwidth()
        window_width = self.page.winfo_width()
        x = (screen_width // 2) - (window_width // 2)
        y = 10
        self.page.geometry(f'+{x}+{y}')

        self.py_manager = PyInstallerFrame(self.page, self.icon_path)
        self.py_manager.setup_tray_icon()

        #self._create_startup_checkbox()
        #self._setup_tray_icon()
        return self.page
