import threading
import pystray
from PIL import Image, ImageDraw

class TrayIconFrame:
    def __init__(self, window, icon_image=None, tooltip="Aplicativo", menu_items=None):
        """
        :param window: Tkinter window instance
        :param icon_image: Icon image (PIL.Image) or None to use default
        :param tooltip: Text that appears when hovering over the icon
        :param menu_items: List of custom menu items
        """
        self.window = window
        self.tray_icon = None
        self.icon_image = self._ensure_icon_image(icon_image)
        self.tooltip = tooltip
        self.menu_items = menu_items or []
        
        # Sets the default behavior on close
        self.window.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        # Set to minimize to tray as well
        self.window.bind("<Unmap>", lambda e: self._check_if_minimized(e))
    
    def _ensure_icon_image(self, icon_image):
        """Ensures we have a valid icon image"""
        if icon_image is not None:
            return icon_image
        
        # Creates a simple icon if none is provided
        width = 64
        height = 64
        color1 = '#1E90FF'
        color2 = '#FFFFFF'
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse((0, 0, width-1, height-1), fill=color1)
        dc.text((width//2, height//2), 'E', fill=color2, anchor='mm')
        
        return image
    
    def _check_if_minimized(self, event):
        """Checks if the window has been minimized"""
        if self.window.state() == "iconic":
            self.minimize_to_tray()
    
    def minimize_to_tray(self):
        """Minimizes the window to the system tray"""
        self.window.withdraw()
        
        menu_items = [
            pystray.MenuItem("Abrir", self.restore_window),
            pystray.Menu.SEPARATOR,
            *self.menu_items,
            pystray.MenuItem("Sair", self.quit_application)
        ]
        
        # To avoid thread issues, we check if the image is OK
        if not hasattr(self.icon_image, 'save'):
            self.icon_image = self._ensure_icon_image(None)
        
        self.tray_icon = pystray.Icon(
            "app_icon", 
            self.icon_image, 
            self.tooltip, 
            pystray.Menu(*menu_items)
        )
        
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()
    
    def restore_window(self, icon=None):
        """Restores the main window"""
        if icon:
            icon.stop()
        
        if not self.window.winfo_exists():
            return
        
        self.window.deiconify()
        self.window.state('normal')
    
    def quit_application(self, icon=None):
        """Closes the application completely"""
        if icon:
            icon.stop()
        
        if self.window.winfo_exists():
            self.window.quit()
            self.window.destroy()
