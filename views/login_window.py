import tkinter as tk
from tkinter import ttk, messagebox
from config import Config
from assets.styles.theme import theme
from controllers.user_controller import UserController

class LoginWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.controller = UserController()
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Logo/Header
        logo_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        logo_frame.pack(pady=(0, 30))
        
        # App title
        title_label = ttk.Label(logo_frame, 
                               text=Config.APP_NAME,
                               style='Title.TLabel',
                               font=('Segoe UI', 20, 'bold'))
        title_label.pack()
        
        version_label = ttk.Label(logo_frame,
                                 text=f"Version {Config.VERSION}",
                                 style='Normal.TLabel',
                                 foreground=Config.THEME['text_secondary'])
        version_label.pack()
        
        # Login form card
        form_card = theme.create_card(self.main_frame)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form content
        form_content = ttk.Frame(form_card, style='Modern.TFrame')
        form_content.pack(padx=30, pady=30)
        
        # Username
        ttk.Label(form_content, text="Username", style='Heading.TLabel').pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(form_content, style='Modern.TEntry', width=25, font=Config.FONTS['normal'])
        self.username_entry.pack(fill='x', pady=(0, 15))
        self.username_entry.focus()
        
        # Password
        ttk.Label(form_content, text="Password", style='Heading.TLabel').pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(form_content, style='Modern.TEntry', width=25, 
                                       show="•", font=Config.FONTS['normal'])
        self.password_entry.pack(fill='x', pady=(0, 20))
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = ttk.Button(form_content, text="Login", style='Modern.TButton',
                              command=self.login)
        login_btn.pack(fill='x', pady=(0, 10))
        
        # Footer
        footer_frame = ttk.Frame(form_content, style='Modern.TFrame')
        footer_frame.pack(fill='x')
        
        ttk.Label(footer_frame, text=f"© 2024 {Config.COMPANY_NAME}", 
                 style='Small.TLabel', foreground=Config.THEME['text_secondary']).pack(side='right')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = self.controller.authenticate(username, password)
        if user:
            self.app.show_main_app(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def show(self):
        self.root.deiconify()