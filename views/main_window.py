import tkinter as tk
from tkinter import ttk
from config import Config
from assets.styles.theme import theme
from .dashboard import Dashboard

class MainWindow:
    def __init__(self, app, user):
        self.app = app
        self.user = user
        self.current_view = None
        
        # Create main window
        self.root = tk.Toplevel(self.app.root)
        self.setup_window()
        self.setup_sidebar()
        self.setup_main_area()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def setup_window(self):
        self.root.title(f"{Config.APP_NAME} - Welcome, {self.user.full_name}")
        self.root.geometry(Config.MAIN_WINDOW_SIZE)
        self.root.configure(bg=Config.THEME['primary'])
        self.root.minsize(1200, 700)
        
        # Center window manually (Toplevel doesn't have eval)
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_sidebar(self):
        # Sidebar frame
        self.sidebar = ttk.Frame(self.root, style='Modern.TFrame', width=250)
        self.sidebar.pack(side='left', fill='y', padx=(0, 1))
        self.sidebar.pack_propagate(False)
        
        # User info
        user_frame = ttk.Frame(self.sidebar, style='Modern.TFrame')
        user_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(user_frame, text=self.user.full_name, 
                 style='Heading.TLabel', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        ttk.Label(user_frame, text=f"@{self.user.username} • {self.user.role.title()}",
                 style='Small.TLabel', foreground=Config.THEME['text_secondary']).pack(anchor='w')
        
        # Separator
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill='x', padx=10, pady=5)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.sidebar, style='Modern.TFrame')
        nav_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Navigation items
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("💰 Sales Voucher", "sales"),
            ("🛒 Purchase Voucher", "purchase"), 
            ("🧾 Receipt Voucher", "receipt"),
            ("💳 Payment Voucher", "payment"),
            ("📒 Ledgers", "ledgers"),
            ("📈 Reports", "reports"),
            ("👥 User Management", "users"),
            ("⚙️ Settings", "settings"),
            ("📋 System Logs", "logs")
        ]
        
        self.nav_buttons = {}
        for text, key in nav_items:
            btn = ttk.Button(nav_frame, text=text, style='Secondary.TButton',
                           command=lambda k=key: self.on_nav_click(k))
            btn.pack(fill='x', pady=2)
            self.nav_buttons[key] = btn
        
        # Logout button at bottom
        logout_frame = ttk.Frame(self.sidebar, style='Modern.TFrame')
        logout_frame.pack(fill='x', side='bottom', padx=10, pady=10)
        
        ttk.Button(logout_frame, text="🚪 Logout", style='Danger.TButton',
                  command=self.logout).pack(fill='x')
    
    def setup_main_area(self):
        # Main content area
        self.main_area = ttk.Frame(self.root, style='Modern.TFrame')
        self.main_area.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    
    def on_nav_click(self, nav_key):
        # Update button states
        for key, btn in self.nav_buttons.items():
            if key == nav_key:
                btn.configure(style='Modern.TButton')
            else:
                btn.configure(style='Secondary.TButton')
        
        # Show appropriate view
        if nav_key == "dashboard":
            self.show_dashboard()
        elif nav_key == "sales":
            self.show_sales_voucher()
        elif nav_key == "purchase":
            self.show_purchase_voucher()
        elif nav_key == "receipt":
            self.show_receipt_voucher()
        elif nav_key == "payment":
            self.show_payment_voucher()
        elif nav_key == "ledgers":
            self.show_ledgers()
        elif nav_key == "reports":
            self.show_reports()
        elif nav_key == "users":
            self.show_user_management()
        elif nav_key == "settings":
            self.show_settings()
        elif nav_key == "logs":
            self.show_system_logs()
    
    def show_dashboard(self):
        self.clear_main_area()
        self.current_view = Dashboard(self.main_area, self.user)
    
    def show_sales_voucher(self):
        self.clear_main_area()
        from .voucher_views.sales_voucher import SalesVoucherView
        self.current_view = SalesVoucherView(self.main_area, self.user)
    
    def show_purchase_voucher(self):
        self.clear_main_area()
        from .voucher_views.purchase_voucher import PurchaseVoucherView
        self.current_view = PurchaseVoucherView(self.main_area, self.user)
    
    def show_receipt_voucher(self):
        self.clear_main_area()
        from .voucher_views.receipt_voucher import ReceiptVoucherView
        self.current_view = ReceiptVoucherView(self.main_area, self.user)
    
    def show_payment_voucher(self):
        self.clear_main_area()
        from .voucher_views.payment_voucher import PaymentVoucherView
        self.current_view = PaymentVoucherView(self.main_area, self.user)
    
    def show_ledgers(self):
        self.clear_main_area()
        from .ledger_views.ledger_main import LedgerMainView
        self.current_view = LedgerMainView(self.main_area, self.user)
    
    def show_reports(self):
        self.clear_main_area()
        from .reports_views.daily_report import DailyReportView
        self.current_view = DailyReportView(self.main_area, self.user)
    
    def show_user_management(self):
        if self.user.role != 'admin':
            tk.messagebox.showwarning("Access Denied", "Only administrators can access user management")
            return
        
        self.clear_main_area()
        from .management_views.user_management import UserManagementView
        self.current_view = UserManagementView(self.main_area, self.user)
    
    def show_settings(self):
        self.clear_main_area()
        from .management_views.company_settings import CompanySettingsView
        self.current_view = CompanySettingsView(self.main_area, self.user)
    
    def show_system_logs(self):
        if self.user.role != 'admin':
            tk.messagebox.showwarning("Access Denied", "Only administrators can access system logs")
            return
        
        self.clear_main_area()
        from .management_views.system_logs import SystemLogsView
        self.current_view = SystemLogsView(self.main_area, self.user)
    
    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.root.destroy()
        self.app.root.deiconify()
    
    def on_close(self):
        self.logout()
    
    def show(self):
        self.root.deiconify()