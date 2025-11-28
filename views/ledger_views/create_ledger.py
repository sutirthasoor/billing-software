import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from config import Config
from assets.styles.theme import theme
from controllers.ledger_controller import LedgerController
from utils.validators import Validators
from utils.constants import LedgerTypes, BalanceTypes

class CreateLedgerView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.ledger_controller = LedgerController()
        
        self.setup_ui()
        self.load_ledger_groups()
    
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
        
        ttk.Label(header_frame, text="Create New Ledger", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Basic Information Card
        basic_card = theme.create_card(self.scrollable_frame)
        basic_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(basic_card, text="Basic Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        basic_frame = ttk.Frame(basic_card, style='Modern.TFrame')
        basic_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Ledger Name
        ttk.Label(basic_frame, text="Ledger Name *", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.name_entry = ttk.Entry(basic_frame, style='Modern.TEntry', width=40)
        self.name_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Ledger Group
        ttk.Label(basic_frame, text="Ledger Group *", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(basic_frame, textvariable=self.group_var,
                                       style='Modern.TCombobox', width=25)
        self.group_combo.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Opening Balance
        ttk.Label(basic_frame, text="Opening Balance", style='Normal.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.opening_balance_entry = ttk.Entry(basic_frame, style='Modern.TEntry', width=20)
        self.opening_balance_entry.insert(0, "0.00")
        self.opening_balance_entry.grid(row=1, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Balance Type
        ttk.Label(basic_frame, text="Balance Type", style='Normal.TLabel').grid(row=1, column=2, sticky='w', pady=8)
        self.balance_type_var = tk.StringVar(value=BalanceTypes.DEBIT)
        balance_frame = ttk.Frame(basic_frame, style='Modern.TFrame')
        balance_frame.grid(row=1, column=3, sticky='w', pady=8, padx=(10, 0))
        
        ttk.Radiobutton(balance_frame, text="Debit", variable=self.balance_type_var, 
                       value=BalanceTypes.DEBIT, style='TRadiobutton').pack(side='left', padx=(0, 10))
        ttk.Radiobutton(balance_frame, text="Credit", variable=self.balance_type_var,
                       value=BalanceTypes.CREDIT, style='TRadiobutton').pack(side='left')
        
        # Contact Information Card
        contact_card = theme.create_card(self.scrollable_frame)
        contact_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(contact_card, text="Contact Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        contact_frame = ttk.Frame(contact_card, style='Modern.TFrame')
        contact_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Contact Person
        ttk.Label(contact_frame, text="Contact Person", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.contact_person_entry = ttk.Entry(contact_frame, style='Modern.TEntry', width=30)
        self.contact_person_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Phone
        ttk.Label(contact_frame, text="Phone", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.phone_entry = ttk.Entry(contact_frame, style='Modern.TEntry', width=20)
        self.phone_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Email
        ttk.Label(contact_frame, text="Email", style='Normal.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.email_entry = ttk.Entry(contact_frame, style='Modern.TEntry', width=30)
        self.email_entry.grid(row=1, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Address
        ttk.Label(contact_frame, text="Address", style='Normal.TLabel').grid(row=2, column=0, sticky='w', pady=8)
        self.address_text = tk.Text(contact_frame, width=50, height=3, font=Config.FONTS['normal'],
                                   bg=Config.THEME['primary'], relief='solid', bd=1)
        self.address_text.grid(row=2, column=1, columnspan=3, sticky='w', pady=8, padx=(10, 0))
        
        # Tax Information Card
        tax_card = theme.create_card(self.scrollable_frame)
        tax_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(tax_card, text="Tax Information", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        tax_frame = ttk.Frame(tax_card, style='Modern.TFrame')
        tax_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # GSTIN
        ttk.Label(tax_frame, text="GSTIN", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.gstin_entry = ttk.Entry(tax_frame, style='Modern.TEntry', width=25)
        self.gstin_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # State
        ttk.Label(tax_frame, text="State", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.state_entry = ttk.Entry(tax_frame, style='Modern.TEntry', width=20)
        self.state_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
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
        
        ttk.Button(btn_frame, text="Clear Form", style='Secondary.TButton',
                  command=self.clear_form).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="Save Ledger", style='Modern.TButton',
                  command=self.save_ledger).pack(side='left')
        
        # Set focus to name field
        self.name_entry.focus()
    
    def load_ledger_groups(self):
        """Load ledger groups for combobox"""
        try:
            groups = self.ledger_controller.get_ledger_groups()
            group_names = [group.name for group in groups]
            self.group_combo['values'] = group_names
            
            # Set default group if available
            if group_names:
                self.group_combo.set(group_names[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledger groups: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        if messagebox.askyesno("Confirm", "Clear all form data?"):
            self.name_entry.delete(0, tk.END)
            self.group_combo.set('')
            self.opening_balance_entry.delete(0, tk.END)
            self.opening_balance_entry.insert(0, "0.00")
            self.balance_type_var.set(BalanceTypes.DEBIT)
            self.contact_person_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.address_text.delete('1.0', tk.END)
            self.gstin_entry.delete(0, tk.END)
            self.state_entry.delete(0, tk.END)
            self.status_var.set('')
            self.name_entry.focus()
    
    def validate_form(self):
        """Validate form data"""
        name = self.name_entry.get().strip()
        group = self.group_var.get().strip()
        opening_balance = self.opening_balance_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        gstin = self.gstin_entry.get().strip()
        
        # Required fields
        if not name:
            messagebox.showerror("Error", "Ledger name is required")
            return False
        
        if not group:
            messagebox.showerror("Error", "Ledger group is required")
            return False
        
        # Validate opening balance
        if not Validators.validate_amount(opening_balance):
            messagebox.showerror("Error", "Invalid opening balance amount")
            return False
        
        # Validate phone if provided
        if phone and not Validators.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format (10 digits required)")
            return False
        
        # Validate email if provided
        if email and not Validators.validate_email(email):
            messagebox.showerror("Error", "Invalid email address format")
            return False
        
        # Validate GSTIN if provided
        if gstin and not Validators.validate_gstin(gstin):
            messagebox.showerror("Error", "Invalid GSTIN format")
            return False
        
        return True
    
    def save_ledger(self):
        """Save the ledger to database"""
        if not self.validate_form():
            return
        
        try:
            # Get form data
            name = self.name_entry.get().strip()
            group_name = self.group_var.get().strip()
            opening_balance = Decimal(self.opening_balance_entry.get().strip())
            balance_type = self.balance_type_var.get()
            contact_person = self.contact_person_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_text.get('1.0', tk.END).strip()
            gstin = self.gstin_entry.get().strip()
            state = self.state_entry.get().strip()
            
            # Get group ID
            groups = self.ledger_controller.get_ledger_groups()
            group = next((g for g in groups if g.name == group_name), None)
            
            if not group:
                messagebox.showerror("Error", "Selected ledger group not found")
                return
            
            # Prepare ledger data
            ledger_data = {
                'name': name,
                'group_id': group.id,
                'opening_balance': float(opening_balance),
                'balance_type': balance_type,
                'contact_person': contact_person,
                'address': address,
                'phone': phone,
                'email': email,
                'gstin': gstin,
                'state': state
            }
            
            # Save ledger
            ledger_id = self.ledger_controller.create_ledger(ledger_data)
            
            if ledger_id:
                messagebox.showinfo("Success", f"Ledger '{name}' created successfully!")
                self.clear_form()
                self.status_var.set("Ledger saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to create ledger. Ledger name might already exist.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create ledger: {str(e)}")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")