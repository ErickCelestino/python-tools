from tkinter import BOTH, ttk
from ..frame.home_frame import HomeFrame

class HomePage:
    def __init__(self):
        self.page_setup = HomeFrame()
        self.page = self.page_setup.window_setup()

        self.render()
    
    def render(self):
        main_frame = ttk.Frame(self.page, padding="10")
        main_frame.pack(fill=BOTH, expand=True)
        
        self.page.mainloop()