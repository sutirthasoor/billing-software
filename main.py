import utils.session
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from views.login_window import LoginWindow
from database import db_instance

class BillingSoftware:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_root_window()
        self.current_user = None
        
    def setup_root_window(self):
        self.root.title(f"{Config.APP_NAME} v{Config.VERSION}")
        self.root.geometry(Config.LOGIN_WINDOW_SIZE)
        self.root.configure(bg=Config.THEME['primary'])
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
    def run(self):
        # Show login window first
        login_window = LoginWindow(self.root, self)
        login_window.show()
        
        self.root.mainloop()
    
    def show_main_app(self, user):
        self.current_user = user
        self.root.withdraw()  # Hide login window
        
        # Import here to avoid circular imports
        from views.main_window import MainWindow
        main_window = MainWindow(self, user)
        main_window.show()

def main():
    # Ensure required directories exist
    Config.ensure_directories()
    
    # Initialize database
    db_instance
    
    # Create and run application
    app = BillingSoftware()
    app.run()

if __name__ == "__main__":
    main()