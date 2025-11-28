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

class PurchaseVoucherView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.voucher_controller = VoucherController()
        self.ledger_controller = LedgerController()
        self.voucher_items = []
        
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
        
        ttk.Label(header_frame, text="Purchase Voucher", 
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
        
        ttk.Label(party_card, text="Supplier Details", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        party_frame = ttk.Frame(party_card, style='Modern.TFrame')
        party_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Label(party_frame, text="Select Supplier:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.party_var = tk.StringVar()
        self.party_combo = ttk.Combobox(party_frame, textvariable=self.party_var, 
                                       style='Modern.TCombobox', width=30)
        self.party_combo.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(party_frame, text="Narration:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.narration_entry = ttk.Entry(party_frame, style='Modern.TEntry', width=30)
        self.narration_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(10, 0))
        
        # Items frame
        items_card = theme.create_card(container)
        items_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(items_card, text="Purchase Items", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        # Items table
        columns = ('ledger', 'amount', 'narration', 'actions')
        self.items_tree = ttk.Treeview(items_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.items_tree.heading('ledger', text='Ledger Account')
        self.items_tree.heading('amount', text='Amount')
        self.items_tree.heading('narration', text='Narration')
        self.items_tree.heading('actions', text='Actions')
        
        self.items_tree.column('ledger', width=300)
        self.items_tree.column('amount', width=150)
        self.items_tree.column('narration', width=200)
        self.items_tree.column('actions', width=100)
        
        scrollbar = ttk.Scrollbar(items_card, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 15))
        
        # Add item form
        add_item_card = theme.create_card(container)
        add_item_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(add_item_card, text="Add Item", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        add_frame = ttk.Frame(add_item_card, style='Modern.TFrame')
        add_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Label(add_frame, text="Ledger:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.ledger_var = tk.StringVar()
        self.ledger_combo = ttk.Combobox(add_frame, textvariable=self.ledger_var,
                                        style='Modern.TCombobox', width=25)
        self.ledger_combo.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(add_frame, text="Amount:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=5)
        self.amount_entry = ttk.Entry(add_frame, style='Modern.TEntry', width=15)
        self.amount_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(10, 20))
        
        ttk.Label(add_frame, text="Narration:", style='Normal.TLabel').grid(row=0, column=4, sticky='w', pady=5)
        self.item_narration_entry = ttk.Entry(add_frame, style='Modern.TEntry', width=20)
        self.item_narration_entry.grid(row=0, column=5, sticky='w', pady=5, padx=(10, 0))
        
        add_btn = ttk.Button(add_frame, text="Add Item", style='Success.TButton',
                           command=self.add_item)
        add_btn.grid(row=0, column=6, sticky='w', pady=5, padx=(20, 0))
        
        # Totals and actions
        footer_card = theme.create_card(container)
        footer_card.pack(fill='x', pady=(0, 10))
        
        footer_frame = ttk.Frame(footer_card, style='Modern.TFrame')
        footer_frame.pack(fill='x', padx=15, pady=15)
        
        # Total amount
        self.total_var = tk.StringVar(value=f"Total: {Config.CURRENCY} 0.00")
        ttk.Label(footer_frame, textvariable=self.total_var, style='Heading.TLabel',
                 foreground=Config.THEME['accent']).pack(side='left')
        
        # Action buttons
        btn_frame = ttk.Frame(footer_frame, style='Modern.TFrame')
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text="Clear", style='Secondary.TButton',
                  command=self.clear_form).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="Save Voucher", style='Modern.TButton',
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
            
            # For purchase items (expense accounts)
            purchase_ledgers = [ledger.name for ledger in ledgers 
                              if any(group in getattr(ledger, 'group_name', '') 
                                   for group in ['Purchase', 'Expense', 'Direct Expenses'])]
            self.ledger_combo['values'] = purchase_ledgers
            
            # Set next voucher number
            next_voucher = self.voucher_controller.get_next_voucher_number(VoucherTypes.PURCHASE)
            self.voucher_no_var.set(next_voucher)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledgers: {str(e)}")
    
    def add_item(self):
        """Add item to voucher"""
        ledger = self.ledger_var.get().strip()
        amount_str = self.amount_entry.get().strip()
        narration = self.item_narration_entry.get().strip()
        
        # Validation
        if not ledger:
            messagebox.showerror("Error", "Please select a ledger account")
            return
        
        if not Validators.validate_amount(amount_str):
            messagebox.showerror("Error", "Please enter a valid amount")
            return
        
        amount = Decimal(amount_str)
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0")
            return
        
        # Add to treeview
        item_id = len(self.voucher_items) + 1
        self.items_tree.insert('', 'end', values=(
            ledger, f"{Config.CURRENCY} {amount:,.2f}", narration, "❌ Remove"
        ))
        
        # Store in memory
        self.voucher_items.append({
            'ledger_name': ledger,
            'amount': amount,
            'narration': narration
        })
        
        # Update total
        self.update_total()
        
        # Clear form
        self.ledger_var.set('')
        self.amount_entry.delete(0, tk.END)
        self.item_narration_entry.delete(0, tk.END)
        
        # Bind remove action
        self.items_tree.bind('<Button-1>', self.on_item_click)
    
    def on_item_click(self, event):
        """Handle item removal"""
        item = self.items_tree.identify_row(event.y)
        column = self.items_tree.identify_column(event.x)
        
        if item and column == '#4':  # Actions column
            if messagebox.askyesno("Confirm", "Remove this item?"):
                # Remove from treeview
                self.items_tree.delete(item)
                
                # Remove from memory
                index = int(item) - 1
                if 0 <= index < len(self.voucher_items):
                    self.voucher_items.pop(index)
                
                # Update total
                self.update_total()
    
    def update_total(self):
        """Update total amount"""
        total = sum(item['amount'] for item in self.voucher_items)
        self.total_var.set(f"Total: {Config.CURRENCY} {total:,.2f}")
    
    def clear_form(self):
        """Clear the entire form"""
        if messagebox.askyesno("Confirm", "Clear all data?"):
            # Clear items
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)
            self.voucher_items.clear()
            
            # Clear form fields
            self.party_var.set('')
            self.narration_entry.delete(0, tk.END)
            self.ledger_var.set('')
            self.amount_entry.delete(0, tk.END)
            self.item_narration_entry.delete(0, tk.END)
            
            # Reset total
            self.update_total()
    
    def save_voucher(self):
        """Save the purchase voucher"""
        # Validation
        if not self.party_var.get().strip():
            messagebox.showerror("Error", "Please select a supplier")
            return
        
        if not self.voucher_items:
            messagebox.showerror("Error", "Please add at least one item")
            return
        
        try:
            # Get party ledger ID
            party_name = self.party_var.get().strip()
            ledgers = self.ledger_controller.get_all_ledgers()
            party_ledger = next((l for l in ledgers if l.name == party_name), None)
            
            if not party_ledger:
                messagebox.showerror("Error", "Selected supplier not found in ledgers")
                return
            
            # Prepare voucher data
            voucher_data = {
                'voucher_type': VoucherTypes.PURCHASE,
                'voucher_number': self.voucher_no_var.get(),
                'voucher_date': datetime.now().date(),
                'party_ledger_id': party_ledger.id,
                'narration': self.narration_entry.get().strip(),
                'total_amount': sum(item['amount'] for item in self.voucher_items),
                'created_by': self.user.id,
                'items': []
            }
            
            # Add credit entry for supplier
            voucher_data['items'].append({
                'ledger_id': party_ledger.id,
                'amount': voucher_data['total_amount'],
                'type': 'Credit',
                'narration': voucher_data['narration']
            })
            
            # Add debit entries for purchase items
            for item in self.voucher_items:
                ledger_name = item['ledger_name']
                ledger = next((l for l in ledgers if l.name == ledger_name), None)
                
                if ledger:
                    voucher_data['items'].append({
                        'ledger_id': ledger.id,
                        'amount': item['amount'],
                        'type': 'Debit',
                        'narration': item['narration']
                    })
            
            # Save voucher
            voucher_id = self.voucher_controller.create_voucher(voucher_data)
            
            if voucher_id:
                messagebox.showinfo("Success", f"Purchase voucher saved successfully!\nVoucher No: {voucher_data['voucher_number']}")
                self.clear_form()
                
                # Refresh voucher number
                next_voucher = self.voucher_controller.get_next_voucher_number(VoucherTypes.PURCHASE)
                self.voucher_no_var.set(next_voucher)
            else:
                messagebox.showerror("Error", "Failed to save voucher")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save voucher: {str(e)}")