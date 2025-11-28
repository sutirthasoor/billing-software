from tkinter import ttk
import tkinter as tk
from config import Config

class ModernTheme:
    def __init__(self):
        self.setup_styles()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure main styles with white theme
        style.configure('Modern.TFrame', background=Config.THEME['primary'])
        style.configure('Card.TFrame', background=Config.THEME['secondary'], relief='raised', borderwidth=1)
        
        # Modern Button Styles
        style.configure('Modern.TButton',
                       background=Config.THEME['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=Config.FONTS['normal'],
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', Config.THEME['accent']),
                           ('pressed', Config.THEME['accent'])])
        
        # Add more style configurations as needed
    
    def create_card(self, parent, **kwargs):
        """Create a modern card widget"""
        card = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return card

# Global theme instance
theme = ModernTheme()