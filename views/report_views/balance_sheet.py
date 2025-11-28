import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import Config
from assets.styles.theme import theme
from controllers.report_controller import ReportController
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class BalanceSheetView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.report_controller = ReportController()
        self.excel_exporter = ExcelExporter()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Balance Sheet", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="As On Date", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Date Selection
        ttk.Label(filters_frame, text="As On Date:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
        self.date_entry = ttk.Entry(filters_frame, textvariable=self.date_var,
                                   style='Modern.TEntry', width=15)
        self.date_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Action Buttons
        action_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=15)
        
        ttk.Button(action_frame, text="Generate Report", style='Modern.TButton',
                  command=self.generate_report).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Export to Excel", style='Success.TButton',
                  command=self.export_to_excel).pack(side='left')
        
        # Report Data Card
        data_card = theme.create_card(container)
        data_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(data_card, text="Balance Sheet", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Balance Sheet Table
        columns = ('liabilities', 'l_amount', 'assets', 'a_amount')
        self.bs_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.bs_tree.heading('liabilities', text='Liabilities')
        self.bs_tree.heading('l_amount', text='Amount')
        self.bs_tree.heading('assets', text='Assets')
        self.bs_tree.heading('a_amount', text='Amount')
        
        self.bs_tree.column('liabilities', width=250)
        self.bs_tree.column('l_amount', width=150)
        self.bs_tree.column('assets', width=250)
        self.bs_tree.column('a_amount', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.bs_tree.yview)
        self.bs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.bs_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select date to generate Balance Sheet")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def generate_report(self):
        """Generate Balance Sheet"""
        try:
            date_str = self.date_var.get().strip()
            
            # Clear previous data
            for item in self.bs_tree.get_children():
                self.bs_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating Balance Sheet...")
            self.parent.update()
            
            # Generate sample Balance Sheet data
            bs_data = self.get_balance_sheet_data(date_str)
            
            # Populate Balance Sheet table
            max_rows = max(len(bs_data['liabilities']), len(bs_data['assets']))
            
            for i in range(max_rows):
                liability = bs_data['liabilities'][i] if i < len(bs_data['liabilities']) else ('', '')
                asset = bs_data['assets'][i] if i < len(bs_data['assets']) else ('', '')
                
                self.bs_tree.insert('', 'end', values=(
                    liability[0], liability[1], asset[0], asset[1]
                ))
            
            self.status_var.set(f"Balance Sheet generated as on {date_str}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def get_balance_sheet_data(self, date_str):
        """Get Balance Sheet data (sample implementation)"""
        # This is sample data - in real implementation, this would calculate from ledger balances
        liabilities = [
            ("CAPITAL & LIABILITIES", ""),
            ("  Capital Account", f"{Config.CURRENCY} 200,000.00"),
            ("  Reserves & Surplus", f"{Config.CURRENCY} 50,000.00"),
            ("  Current Liabilities", f"{Config.CURRENCY} 75,000.00"),
            ("  Loans", f"{Config.CURRENCY} 100,000.00"),
            ("  Total Liabilities", f"{Config.CURRENCY} 425,000.00")
        ]
        
        assets = [
            ("ASSETS", ""),
            ("  Fixed Assets", f"{Config.CURRENCY} 150,000.00"),
            ("  Current Assets", f"{Config.CURRENCY} 200,000.00"),
            ("  Investments", f"{Config.CURRENCY} 50,000.00"),
            ("  Cash & Bank", f"{Config.CURRENCY} 25,000.00"),
            ("  Total Assets", f"{Config.CURRENCY} 425,000.00")
        ]
        
        return {'liabilities': liabilities, 'assets': assets}
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.bs_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            date_str = self.date_var.get().strip()
            
            # Prepare data for export
            data = []
            headers = ['Liabilities', 'Amount', 'Assets', 'Amount']
            data.append(headers)
            
            for item in self.bs_tree.get_children():
                values = self.bs_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Balance_Sheet_{date_str}.xlsx"
            success, result = self.excel_exporter.export_balance_sheet(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")