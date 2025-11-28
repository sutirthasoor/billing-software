import tkinter as tk
from tkinter import ttk
from config import Config
from assets.styles.theme import theme

class SystemLogsView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(container, text="System Logs - Coming Soon", 
                 style='Title.TLabel').pack(pady=20)