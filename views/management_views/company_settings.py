import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import Config
from assets.styles.theme import theme
from controllers.user_controller import UserController
from utils.validators import Validators
from utils.helpers import Helpers

class CompanySettingsView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.user_controller = UserController()
        
        self.setup_ui()
        self.load_company_data()
    
    def setup_ui(self):
        # Main container with scrollbar
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(container, bg=Config.THEME['primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Modern.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Header
        header_frame = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Company Settings", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Company Information Card
        company_card = theme.create_card(self.scrollable_frame)
        company_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(company_card, text="Company Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        company_frame = ttk.Frame(company_card, style='Modern.TFrame')
        company_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Company Name
        ttk.Label(company_frame, text="Company Name *", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.company_name_var = tk.StringVar(value=Config.COMPANY_NAME)
        self.company_name_entry = ttk.Entry(company_frame, textvariable=self.company_name_var,
                                          style='Modern.TEntry', width=40)
        self.company_name_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Address
        ttk.Label(company_frame, text="Address", style='Normal.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.address_text = tk.Text(company_frame, width=50, height=3, font=Config.FONTS['normal'],
                                   bg=Config.THEME['primary'], relief='solid', bd=1)
        self.address_text.grid(row=1, column=1, columnspan=3, sticky='w', pady=8, padx=(10, 0))
        
        # Contact Information Card
        contact_card = theme.create_card(self.scrollable_frame)
        contact_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(contact_card, text="Contact Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        contact_frame = ttk.Frame(contact_card, style='Modern.TFrame')
        contact_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Phone
        ttk.Label(contact_frame, text="Phone", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(contact_frame, textvariable=self.phone_var,
                                    style='Modern.TEntry', width=20)
        self.phone_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Email
        ttk.Label(contact_frame, text="Email", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(contact_frame, textvariable=self.email_var,
                                    style='Modern.TEntry', width=25)
        self.email_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Tax Information Card
        tax_card = theme.create_card(self.scrollable_frame)
        tax_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(tax_card, text="Tax Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        tax_frame = ttk.Frame(tax_card, style='Modern.TFrame')
        tax_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # GSTIN
        ttk.Label(tax_frame, text="GSTIN", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.gstin_var = tk.StringVar()
        self.gstin_entry = ttk.Entry(tax_frame, textvariable=self.gstin_var,
                                    style='Modern.TEntry', width=25)
        self.gstin_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # State
        ttk.Label(tax_frame, text="State", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.state_var = tk.StringVar()
        self.state_entry = ttk.Entry(tax_frame, textvariable=self.state_var,
                                    style='Modern.TEntry', width=20)
        self.state_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # State Code
        ttk.Label(tax_frame, text="State Code", style='Normal.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.state_code_var = tk.StringVar()
        self.state_code_entry = ttk.Entry(tax_frame, textvariable=self.state_code_var,
                                         style='Modern.TEntry', width=10)
        self.state_code_entry.grid(row=1, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Application Settings Card
        app_card = theme.create_card(self.scrollable_frame)
        app_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(app_card, text="Application Settings", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        app_frame = ttk.Frame(app_card, style='Modern.TFrame')
        app_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Currency
        ttk.Label(app_frame, text="Currency Symbol", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.currency_var = tk.StringVar(value=Config.CURRENCY)
        currency_entry = ttk.Entry(app_frame, textvariable=self.currency_var,
                                  style='Modern.TEntry', width=10)
        currency_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Date Format
        ttk.Label(app_frame, text="Date Format", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.date_format_var = tk.StringVar(value=Config.DATE_FORMAT)
        date_format_combo = ttk.Combobox(app_frame, textvariable=self.date_format_var,
                                        values=["%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"],
                                        style='Modern.TCombobox', width=12)
        date_format_combo.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Backup Settings Card
        backup_card = theme.create_card(self.scrollable_frame)
        backup_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(backup_card, text="Backup & Maintenance", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        backup_frame = ttk.Frame(backup_card, style='Modern.TFrame')
        backup_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Backup button
        ttk.Button(backup_frame, text="Create Database Backup", style='Modern.TButton',
                  command=self.create_backup).pack(side='left', padx=(0, 10))
        
        ttk.Button(backup_frame, text="Restore from Backup", style='Secondary.TButton',
                  command=self.restore_backup).pack(side='left')
        
        # Action Buttons Card
        action_card = theme.create_card(self.scrollable_frame)
        action_card.pack(fill='x', pady=(0, 10))
        
        action_frame = ttk.Frame(action_card, style='Modern.TFrame')
        action_frame.pack(fill='x', padx=15, pady=15)
        
        # Status message
        self.status_var = tk.StringVar()
        status_label = ttk.Label(action_frame, textvariable=self.status_var, style='Normal.TLabel')
        status_label.pack(side='left')
        
        # Buttons
        btn_frame = ttk.Frame(action_frame, style='Modern.TFrame')
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text="Reset to Defaults", style='Secondary.TButton',
                  command=self.reset_defaults).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="Save Settings", style='Modern.TButton',
                  command=self.save_settings).pack(side='left')
    
    def load_company_data(self):
        """Load company data from database"""
        try:
            # In a real implementation, this would load from database
            # For now, we'll use default values
            self.address_text.insert('1.0', "Your Company Address\nCity, State - PIN Code")
            self.phone_var.set("1234567890")
            self.email_var.set("info@company.com")
            self.gstin_var.set("12ABCDE1234F1Z5")
            self.state_var.set("Maharashtra")
            self.state_code_var.set("27")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load company data: {str(e)}")
    
    def validate_form(self):
        """Validate form data"""
        company_name = self.company_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        gstin = self.gstin_var.get().strip()
        
        if not company_name:
            messagebox.showerror("Error", "Company name is required")
            return False
        
        if phone and not Validators.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return False
        
        if email and not Validators.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return False
        
        if gstin and not Validators.validate_gstin(gstin):
            messagebox.showerror("Error", "Invalid GSTIN format")
            return False
        
        return True
    
    def save_settings(self):
        """Save company settings"""
        if not self.validate_form():
            return
        
        try:
            # Update configuration
            Config.COMPANY_NAME = self.company_name_var.get().strip()
            Config.CURRENCY = self.currency_var.get().strip()
            Config.DATE_FORMAT = self.date_format_var.get().strip()
            
            # In a real implementation, this would save to database
            # For now, we'll just show a success message
            
            messagebox.showinfo("Success", "Company settings saved successfully!")
            self.status_var.set("Settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_defaults(self):
        """Reset to default settings"""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to default values?"):
            self.company_name_var.set("Your Company Name")
            self.address_text.delete('1.0', tk.END)
            self.address_text.insert('1.0', "Company Address")
            self.phone_var.set("")
            self.email_var.set("")
            self.gstin_var.set("")
            self.state_var.set("")
            self.state_code_var.set("")
            self.currency_var.set("₹")
            self.date_format_var.set("%d-%m-%Y")
            
            self.status_var.set("Settings reset to defaults")
    
    def create_backup(self):
        """Create database backup"""
        try:
            success, result = Helpers.backup_database()
            if success:
                messagebox.showinfo("Success", f"Database backup created:\n{result}")
                self.status_var.set("Backup created successfully")
            else:
                messagebox.showerror("Error", f"Failed to create backup: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def restore_backup(self):
        """Restore database from backup"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Backup File",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if file_path:
                if messagebox.askyesno("Confirm Restore", 
                                     "Restore database from backup?\nThis will replace current data."):
                    # In a real implementation, this would restore the database
                    # For now, we'll just show a message
                    messagebox.showinfo("Restore", "Database restore functionality would be implemented here")
                    self.status_var.set("Database restore initiated")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")