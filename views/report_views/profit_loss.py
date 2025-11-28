import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import Config
from assets.styles.theme import theme
from controllers.report_controller import ReportController
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class ProfitLossView:
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
        
        ttk.Label(header_frame, text="Profit & Loss Statement", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="Select Period", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Period Selection
        ttk.Label(filters_frame, text="From Date:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.from_date_var = tk.StringVar(value="01-04-2024")  # Start of financial year
        self.from_date_entry = ttk.Entry(filters_frame, textvariable=self.from_date_var,
                                        style='Modern.TEntry', width=12)
        self.from_date_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        ttk.Label(filters_frame, text="To Date:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.to_date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
        self.to_date_entry = ttk.Entry(filters_frame, textvariable=self.to_date_var,
                                      style='Modern.TEntry', width=12)
        self.to_date_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Action Buttons
        action_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, columnspan=4, sticky='w', pady=15)
        
        ttk.Button(action_frame, text="Generate Report", style='Modern.TButton',
                  command=self.generate_report).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Export to Excel", style='Success.TButton',
                  command=self.export_to_excel).pack(side='left')
        
        # Report Data Card
        data_card = theme.create_card(container)
        data_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(data_card, text="Profit & Loss Statement", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # P&L Table
        columns = ('particulars', 'amount')
        self.pl_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.pl_tree.heading('particulars', text='Particulars')
        self.pl_tree.heading('amount', text='Amount')
        
        self.pl_tree.column('particulars', width=400)
        self.pl_tree.column('amount', width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.pl_tree.yview)
        self.pl_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pl_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select period to generate Profit & Loss statement")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def generate_report(self):
        """Generate Profit & Loss statement"""
        try:
            from_date = self.from_date_var.get().strip()
            to_date = self.to_date_var.get().strip()
            
            # Clear previous data
            for item in self.pl_tree.get_children():
                self.pl_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating Profit & Loss statement...")
            self.parent.update()
            
            # Generate sample P&L data
            pl_data = self.get_profit_loss_data(from_date, to_date)
            
            # Populate P&L table
            for item in pl_data:
                self.pl_tree.insert('', 'end', values=item)
            
            self.status_var.set(f"Profit & Loss statement generated for period {from_date} to {to_date}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def get_profit_loss_data(self, from_date, to_date):
        """Get Profit & Loss data (sample implementation)"""
        # This is sample data - in real implementation, this would calculate from ledger balances
        pl_data = [
            ("INCOME", ""),
            ("  Sales", f"{Config.CURRENCY} 500,000.00"),
            ("  Other Income", f"{Config.CURRENCY} 25,000.00"),
            ("  Total Income", f"{Config.CURRENCY} 525,000.00"),
            ("", ""),
            ("EXPENSES", ""),
            ("  Purchase", f"{Config.CURRENCY} 300,000.00"),
            ("  Direct Expenses", f"{Config.CURRENCY} 50,000.00"),
            ("  Salary & Wages", f"{Config.CURRENCY} 75,000.00"),
            ("  Rent", f"{Config.CURRENCY} 25,000.00"),
            ("  Utilities", f"{Config.CURRENCY} 15,000.00"),
            ("  Other Expenses", f"{Config.CURRENCY} 10,000.00"),
            ("  Total Expenses", f"{Config.CURRENCY} 475,000.00"),
            ("", ""),
            ("GROSS PROFIT/LOSS", f"{Config.CURRENCY} 50,000.00"),
            ("", ""),
            ("NET PROFIT/LOSS", f"{Config.CURRENCY} 50,000.00")
        ]
        
        return pl_data
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.pl_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            from_date = self.from_date_var.get().strip()
            to_date = self.to_date_var.get().strip()
            
            # Prepare data for export
            data = []
            headers = ['Particulars', 'Amount']
            data.append(headers)
            
            for item in self.pl_tree.get_children():
                values = self.pl_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Profit_Loss_{from_date}_to_{to_date}.xlsx"
            success, result = self.excel_exporter.export_profit_loss(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")