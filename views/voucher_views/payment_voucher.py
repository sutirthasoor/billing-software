import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal
from config import Config
from assets.styles.theme import theme
from controllers.voucher_controller import VoucherController
from controllers.ledger_controller import LedgerController
from utils.validators import Validators
from utils.constants import VoucherTypes

class PaymentVoucherView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.voucher_controller = VoucherController()
        self.ledger_controller = LedgerController()
        
        self.setup_ui()
        self.load_ledgers()
    
    def setup_ui(self):

	self.voucher_no_var = tk.StringVar(value="Auto-generated")
    	self.date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
    	self.party_var = tk.StringVar()
    	self.ledger_var = tk.StringVar()
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Payment Voucher", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Voucher info frame
        info_card = theme.create_card(container)
        info_card.pack(fill='x', pady=(0, 10))
        
        info_frame = ttk.Frame(info_card, style='Modern.TFrame')
        info_frame.pack(fill='x', padx=15, pady=15)
        
        # Voucher number and date
        ttk.Label(info_frame, text="Voucher No:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.voucher_no_var = tk.StringVar(value="Auto-generated")
        ttk.Label(info_frame, textvariable=self.voucher_no_var, style='Normal.TLabel',
                 foreground=Config.THEME['accent']).grid(row=0, column=1, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(info_frame, text="Date:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
        ttk.Label(info_frame, textvariable=self.date_var, style='Normal.TLabel').grid(row=0, column=3, sticky='w', pady=5, padx=(10, 0))
        
        # Party details
        party_card = theme.create_card(container)
        party_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(party_card, text="Paid To", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        party_frame = ttk.Frame(party_card, style='Modern.TFrame')
        party_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Label(party_frame, text="Select Party:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.party_var = tk.StringVar()
        self.party_combo = ttk.Combobox(party_frame, textvariable=self.party_var, 
                                       style='Modern.TCombobox', width=30)
        self.party_combo.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(party_frame, text="Amount:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.amount_entry = ttk.Entry(party_frame, style='Modern.TEntry', width=15)
        self.amount_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(party_frame, text="Narration:", style='Normal.TLabel').grid(row=0, column=4, sticky='w', pady=5)
        self.narration_entry = ttk.Entry(party_frame, style='Modern.TEntry', width=25)
        self.narration_entry.grid(row=0, column=5, sticky='w', pady=5, padx=(10, 0))
        
        # Account details
        account_card = theme.create_card(container)
        account_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(account_card, text="Bank/Cash Account", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        account_frame = ttk.Frame(account_card, style='Modern.TFrame')
        account_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Label(account_frame, text="Select Account:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.account_var = tk.StringVar()
        self.account_combo = ttk.Combobox(account_frame, textvariable=self.account_var,
                                         style='Modern.TCombobox', width=30)
        self.account_combo.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Action buttons
        action_card = theme.create_card(container)
        action_card.pack(fill='x', pady=(0, 10))
        
        action_frame = ttk.Frame(action_card, style='Modern.TFrame')
        action_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Button(action_frame, text="Clear", style='Secondary.TButton',
                  command=self.clear_form).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Save Payment", style='Modern.TButton',
                  command=self.save_voucher).pack(side='left')
    
    def load_ledgers(self):
        """Load ledgers for comboboxes"""
        try:
            ledgers = self.ledger_controller.get_all_ledgers()
            
            # For party (creditors/suppliers)
            party_ledgers = [ledger.name for ledger in ledgers 
                           if any(group in getattr(ledger, 'group_name', '') 
                                for group in ['Sundry Creditors', 'Suppliers'])]
            self.party_combo['values'] = party_ledgers
            
            # For bank/cash accounts
            bank_ledgers = [ledger.name for ledger in ledgers 
                          if any(group in getattr(ledger, 'group_name', '') 
                               for group in ['Bank Accounts', 'Cash-in-Hand'])]
            self.account_combo['values'] = bank_ledgers
            
            # Set next voucher number
            next_voucher = self.voucher_controller.get_next_voucher_number(VoucherTypes.PAYMENT)
            self.voucher_no_var.set(next_voucher)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledgers: {str(e)}")
    
    def clear_form(self):
        """Clear the form"""
        if messagebox.askyesno("Confirm", "Clear all data?"):
            self.party_var.set('')
            self.amount_entry.delete(0, tk.END)
            self.narration_entry.delete(0, tk.END)
            self.account_var.set('')
    
    def save_voucher(self):
        """Save the payment voucher"""
        # Validation
        if not self.party_var.get().strip():
            messagebox.showerror("Error", "Please select a party")
            return
        
        if not self.account_var.get().strip():
            messagebox.showerror("Error", "Please select a bank/cash account")
            return
        
        amount_str = self.amount_entry.get().strip()
        if not Validators.validate_amount(amount_str):
            messagebox.showerror("Error", "Please enter a valid amount")
            return
        
        amount = Decimal(amount_str)
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0")
            return
        
        try:
            # Get ledger IDs
            party_name = self.party_var.get().strip()
            account_name = self.account_var.get().strip()
            
            ledgers = self.ledger_controller.get_all_ledgers()
            
            party_ledger = next((l for l in ledgers if l.name == party_name), None)
            account_ledger = next((l for l in ledgers if l.name == account_name), None)
            
            if not party_ledger or not account_ledger:
                messagebox.showerror("Error", "Selected party or account not found")
                return
            
            # Prepare voucher data
            voucher_data = {
                'voucher_type': VoucherTypes.PAYMENT,
                'voucher_number': self.voucher_no_var.get(),
                'voucher_date': datetime.now().date(),
                'party_ledger_id': party_ledger.id,
                'narration': self.narration_entry.get().strip(),
                'total_amount': amount,
                'created_by': self.user.id,
                'items': [
                    {
                        'ledger_id': party_ledger.id,  # Party account (Debit)
                        'amount': amount,
                        'type': 'Debit',
                        'narration': self.narration_entry.get().strip()
                    },
                    {
                        'ledger_id': account_ledger.id,  # Bank/Cash account (Credit)
                        'amount': amount,
                        'type': 'Credit',
                        'narration': self.narration_entry.get().strip()
                    }
                ]
            }
            
            # Save voucher
            voucher_id = self.voucher_controller.create_voucher(voucher_data)
            
            if voucher_id:
                messagebox.showinfo("Success", f"Payment voucher saved successfully!\nVoucher No: {voucher_data['voucher_number']}")
                self.clear_form()
                
                # Refresh voucher number
                next_voucher = self.voucher_controller.get_next_voucher_number(VoucherTypes.PAYMENT)
                self.voucher_no_var.set(next_voucher)
            else:
                messagebox.showerror("Error", "Failed to save voucher")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save voucher: {str(e)}")