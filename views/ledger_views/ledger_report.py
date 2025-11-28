import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from config import Config
from assets.styles.theme import theme
from controllers.ledger_controller import LedgerController
from controllers.report_controller import ReportController
from utils.printers import print_manager
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class LedgerReportView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.ledger_controller = LedgerController()
        self.report_controller = ReportController()
        self.excel_exporter = ExcelExporter()
        
        self.setup_ui()
        self.load_ledgers()
    
    def setup_ui(self):
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Ledger Report", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="Report Filters", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Ledger Selection
        ttk.Label(filters_frame, text="Select Ledger:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.ledger_var = tk.StringVar()
        self.ledger_combo = ttk.Combobox(filters_frame, textvariable=self.ledger_var,
                                        style='Modern.TCombobox', width=35)
        self.ledger_combo.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Date Range
        ttk.Label(filters_frame, text="From Date:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.from_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime(Config.DATE_FORMAT))
        self.from_date_entry = ttk.Entry(filters_frame, textvariable=self.from_date_var,
                                        style='Modern.TEntry', width=12)
        self.from_date_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 20))
        
        ttk.Label(filters_frame, text="To Date:", style='Normal.TLabel').grid(row=0, column=4, sticky='w', pady=8)
        self.to_date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
        self.to_date_entry = ttk.Entry(filters_frame, textvariable=self.to_date_var,
                                      style='Modern.TEntry', width=12)
        self.to_date_entry.grid(row=0, column=5, sticky='w', pady=8, padx=(10, 0))
        
        # Action Buttons
        action_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, columnspan=6, sticky='w', pady=15)
        
        ttk.Button(action_frame, text="Generate Report", style='Modern.TButton',
                  command=self.generate_report).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Clear Filters", style='Secondary.TButton',
                  command=self.clear_filters).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Export to Excel", style='Success.TButton',
                  command=self.export_to_excel).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Print Report", style='Secondary.TButton',
                  command=self.print_report).pack(side='left')
        
        # Report Summary Card
        self.summary_card = theme.create_card(container)
        self.summary_card.pack(fill='x', pady=(0, 10))
        
        self.summary_frame = ttk.Frame(self.summary_card, style='Modern.TFrame')
        self.summary_frame.pack(fill='x', padx=15, pady=15)
        
        # Initially hide summary
        self.summary_card.pack_forget()
        
        # Report Data Card
        data_card = theme.create_card(container)
        data_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(data_card, text="Ledger Transactions", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Transactions Table
        columns = ('date', 'voucher_no', 'voucher_type', 'narration', 'debit', 'credit', 'balance')
        self.transactions_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.transactions_tree.heading('date', text='Date')
        self.transactions_tree.heading('voucher_no', text='Voucher No')
        self.transactions_tree.heading('voucher_type', text='Type')
        self.transactions_tree.heading('narration', text='Narration')
        self.transactions_tree.heading('debit', text='Debit')
        self.transactions_tree.heading('credit', text='Credit')
        self.transactions_tree.heading('balance', text='Balance')
        
        self.transactions_tree.column('date', width=100)
        self.transactions_tree.column('voucher_no', width=120)
        self.transactions_tree.column('voucher_type', width=100)
        self.transactions_tree.column('narration', width=200)
        self.transactions_tree.column('debit', width=100)
        self.transactions_tree.column('credit', width=100)
        self.transactions_tree.column('balance', width=120)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.transactions_tree.yview)
        h_scrollbar = ttk.Scrollbar(data_card, orient='horizontal', command=self.transactions_tree.xview)
        self.transactions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.transactions_tree.pack(side='top', fill='both', expand=True, padx=15, pady=(0, 5))
        v_scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 5))
        h_scrollbar.pack(side='bottom', fill='x', padx=15, pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select a ledger and date range to generate report")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def load_ledgers(self):
        """Load ledgers for combobox"""
        try:
            ledgers = self.ledger_controller.get_all_ledgers()
            ledger_names = [ledger.name for ledger in ledgers]
            self.ledger_combo['values'] = ledger_names
            
            # Set default if available
            if ledger_names:
                self.ledger_combo.set(ledger_names[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledgers: {str(e)}")
    
    def clear_filters(self):
        """Clear all filters"""
        self.ledger_combo.set('')
        self.from_date_var.set((datetime.now() - timedelta(days=30)).strftime(Config.DATE_FORMAT))
        self.to_date_var.set(datetime.now().strftime(Config.DATE_FORMAT))
        
        # Clear report data
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        # Hide summary
        self.summary_card.pack_forget()
        self.status_var.set("Select a ledger and date range to generate report")
    
    def validate_filters(self):
        """Validate report filters"""
        ledger = self.ledger_var.get().strip()
        from_date = self.from_date_var.get().strip()
        to_date = self.to_date_var.get().strip()
        
        if not ledger:
            messagebox.showerror("Error", "Please select a ledger")
            return False
        
        if not from_date or not to_date:
            messagebox.showerror("Error", "Please select both from and to dates")
            return False
        
        try:
            from_date_obj = Helpers.parse_date(from_date)
            to_date_obj = Helpers.parse_date(to_date)
            
            if from_date_obj > to_date_obj:
                messagebox.showerror("Error", "From date cannot be after to date")
                return False
                
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY")
            return False
        
        return True
    
    def generate_report(self):
        """Generate ledger report"""
        if not self.validate_filters():
            return
        
        try:
            # Get selected ledger
            ledger_name = self.ledger_var.get().strip()
            from_date = self.from_date_var.get().strip()
            to_date = self.to_date_var.get().strip()
            
            ledgers = self.ledger_controller.get_all_ledgers()
            selected_ledger = next((l for l in ledgers if l.name == ledger_name), None)
            
            if not selected_ledger:
                messagebox.showerror("Error", "Selected ledger not found")
                return
            
            # Clear previous data
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating report...")
            self.parent.update()
            
            # Get transactions (this would be from database in real implementation)
            # For now, we'll create sample data
            transactions = self.get_sample_transactions(selected_ledger, from_date, to_date)
            
            if not transactions:
                self.status_var.set(f"No transactions found for {ledger_name} in the selected period")
                self.summary_card.pack_forget()
                return
            
            # Calculate totals
            total_debit = sum(t[4] for t in transactions if t[4])
            total_credit = sum(t[5] for t in transactions if t[5])
            opening_balance = float(selected_ledger.opening_balance)
            
            if selected_ledger.balance_type == 'Debit':
                closing_balance = opening_balance + total_debit - total_credit
            else:
                closing_balance = opening_balance + total_credit - total_debit
            
            # Update summary
            self.update_summary(selected_ledger, opening_balance, total_debit, total_credit, closing_balance)
            
            # Populate transactions table
            running_balance = opening_balance
            
            for trans in transactions:
                date, voucher_no, voucher_type, narration, debit, credit = trans
                
                if selected_ledger.balance_type == 'Debit':
                    running_balance += (debit or 0) - (credit or 0)
                else:
                    running_balance += (credit or 0) - (debit or 0)
                
                self.transactions_tree.insert('', 'end', values=(
                    date,
                    voucher_no,
                    voucher_type,
                    narration,
                    f"{Config.CURRENCY} {debit:,.2f}" if debit else "",
                    f"{Config.CURRENCY} {credit:,.2f}" if credit else "",
                    f"{Config.CURRENCY} {running_balance:,.2f}"
                ))
            
            self.status_var.set(f"Report generated for {ledger_name} - {len(transactions)} transactions found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def update_summary(self, ledger, opening_balance, total_debit, total_credit, closing_balance):
        """Update report summary"""
        # Clear previous summary
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Create summary items
        summary_items = [
            ("Ledger Name:", ledger.name),
            ("Period:", f"{self.from_date_var.get()} to {self.to_date_var.get()}"),
            ("Opening Balance:", f"{Config.CURRENCY} {opening_balance:,.2f}"),
            ("Total Debit:", f"{Config.CURRENCY} {total_debit:,.2f}"),
            ("Total Credit:", f"{Config.CURRENCY} {total_credit:,.2f}"),
            ("Closing Balance:", f"{Config.CURRENCY} {closing_balance:,.2f}")
        ]
        
        for i, (label, value) in enumerate(summary_items):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(self.summary_frame, text=label, style='Normal.TLabel',
                     font=('Segoe UI', 9, 'bold')).grid(row=row, column=col, sticky='w', pady=5, padx=(0, 5))
            
            ttk.Label(self.summary_frame, text=value, style='Normal.TLabel').grid(row=row, column=col+1, sticky='w', pady=5, padx=(0, 20))
        
        # Show summary card
        self.summary_card.pack(fill='x', pady=(0, 10))
    
    def get_sample_transactions(self, ledger, from_date, to_date):
        """Get sample transactions for demonstration"""
        # In real implementation, this would query the database
        # For now, return sample data
        sample_transactions = [
            ("01-01-2024", "SL/0001", "Sales", "Sale to Customer A", 5000.00, 0, None),
            ("05-01-2024", "RCP/0001", "Receipt", "Payment received", 0, 3000.00, None),
            ("10-01-2024", "SL/0002", "Sales", "Sale to Customer B", 7500.00, 0, None),
            ("15-01-2024", "RCP/0002", "Receipt", "Full payment", 0, 9500.00, None),
            ("20-01-2024", "SL/0003", "Sales", "Sale to Customer C", 3200.00, 0, None),
        ]
        
        return sample_transactions
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.transactions_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            # Get selected ledger and dates
            ledger_name = self.ledger_var.get().strip()
            from_date = self.from_date_var.get().strip()
            to_date = self.to_date_var.get().strip()
            
            # Prepare data for export
            data = []
            headers = ['Date', 'Voucher No', 'Voucher Type', 'Narration', 'Debit', 'Credit', 'Balance']
            data.append(headers)
            
            for item in self.transactions_tree.get_children():
                values = self.transactions_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Ledger_Report_{ledger_name}_{from_date}_to_{to_date}.xlsx"
            success, result = self.excel_exporter.export_ledger_report(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def print_report(self):
        """Print the ledger report"""
        if not self.transactions_tree.get_children():
            messagebox.showwarning("Warning", "No data to print. Please generate a report first.")
            return
        
        try:
            # Get selected ledger
            ledger_name = self.ledger_var.get().strip()
            from_date = self.from_date_var.get().strip()
            to_date = self.to_date_var.get().strip()
            
            ledgers = self.ledger_controller.get_all_ledgers()
            selected_ledger = next((l for l in ledgers if l.name == ledger_name), None)
            
            if not selected_ledger:
                messagebox.showerror("Error", "Selected ledger not found")
                return
            
            # Prepare transactions data
            transactions = []
            for item in self.transactions_tree.get_children():
                values = self.transactions_tree.item(item)['values']
                transactions.append(values)
            
            # Print using print manager
            print_manager.print_ledger_report(selected_ledger, transactions, from_date, to_date)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")