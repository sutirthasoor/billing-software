import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import Config
from assets.styles.theme import theme
from controllers.report_controller import ReportController
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class YearlyReportView:
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
        
        ttk.Label(header_frame, text="Yearly Summary Report", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="Select Financial Year", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Financial Year Selection
        ttk.Label(filters_frame, text="Financial Year:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        current_year = datetime.now().year
        # Indian financial year: April to March
        financial_years = [f"{year}-{year+1}" for year in range(current_year-5, current_year+1)]
        self.fy_var = tk.StringVar(value=f"{current_year-1}-{current_year}")
        fy_combo = ttk.Combobox(filters_frame, textvariable=self.fy_var,
                               values=financial_years, style='Modern.TCombobox', width=15)
        fy_combo.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
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
        
        ttk.Label(data_card, text="Yearly Voucher Summary", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Summary Table
        columns = ('month', 'sales', 'purchase', 'receipt', 'payment', 'journal', 'total')
        self.summary_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.summary_tree.heading('month', text='Month')
        self.summary_tree.heading('sales', text='Sales')
        self.summary_tree.heading('purchase', text='Purchase')
        self.summary_tree.heading('receipt', text='Receipt')
        self.summary_tree.heading('payment', text='Payment')
        self.summary_tree.heading('journal', text='Journal')
        self.summary_tree.heading('total', text='Total')
        
        self.summary_tree.column('month', width=120)
        self.summary_tree.column('sales', width=100)
        self.summary_tree.column('purchase', width=100)
        self.summary_tree.column('receipt', width=100)
        self.summary_tree.column('payment', width=100)
        self.summary_tree.column('journal', width=100)
        self.summary_tree.column('total', width=120)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.summary_tree.yview)
        h_scrollbar = ttk.Scrollbar(data_card, orient='horizontal', command=self.summary_tree.xview)
        self.summary_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.summary_tree.pack(side='top', fill='both', expand=True, padx=15, pady=(0, 5))
        v_scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 5))
        h_scrollbar.pack(side='bottom', fill='x', padx=15, pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select financial year to generate yearly report")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def generate_report(self):
        """Generate yearly report"""
        try:
            fy_str = self.fy_var.get()
            start_year = int(fy_str.split('-')[0])
            
            # Clear previous data
            for item in self.summary_tree.get_children():
                self.summary_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating yearly report...")
            self.parent.update()
            
            # Generate sample data (in real implementation, this would query the database)
            yearly_data = self.get_yearly_data(start_year)
            
            if not yearly_data:
                self.status_var.set(f"No data found for financial year {fy_str}")
                return
            
            # Populate summary table
            total_sales = total_purchase = total_receipt = total_payment = total_journal = 0
            
            for month_data in yearly_data:
                self.summary_tree.insert('', 'end', values=(
                    month_data['month'],
                    f"{Config.CURRENCY} {month_data['sales']:,.2f}",
                    f"{Config.CURRENCY} {month_data['purchase']:,.2f}",
                    f"{Config.CURRENCY} {month_data['receipt']:,.2f}",
                    f"{Config.CURRENCY} {month_data['payment']:,.2f}",
                    f"{Config.CURRENCY} {month_data['journal']:,.2f}",
                    f"{Config.CURRENCY} {month_data['total']:,.2f}"
                ))
                
                total_sales += month_data['sales']
                total_purchase += month_data['purchase']
                total_receipt += month_data['receipt']
                total_payment += month_data['payment']
                total_journal += month_data['journal']
            
            # Add totals row
            grand_total = total_sales + total_purchase + total_receipt + total_payment + total_journal
            self.summary_tree.insert('', 'end', values=(
                "TOTAL",
                f"{Config.CURRENCY} {total_sales:,.2f}",
                f"{Config.CURRENCY} {total_purchase:,.2f}",
                f"{Config.CURRENCY} {total_receipt:,.2f}",
                f"{Config.CURRENCY} {total_payment:,.2f}",
                f"{Config.CURRENCY} {total_journal:,.2f}",
                f"{Config.CURRENCY} {grand_total:,.2f}"
            ), tags=('total',))
            
            # Style the total row
            self.summary_tree.tag_configure('total', background=Config.THEME['hover'])
            
            self.status_var.set(f"Yearly report generated for financial year {fy_str}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def get_yearly_data(self, start_year):
        """Get yearly data (sample implementation)"""
        months = [
            "April", "May", "June", "July", "August", "September",
            "October", "November", "December", "January", "February", "March"
        ]
        
        data = []
        for i, month in enumerate(months):
            # Sample data - in real implementation, this would come from database
            sales = (i + 1) * 10000
            purchase = (i + 1) * 8000
            receipt = (i + 1) * 5000
            payment = (i + 1) * 4500
            journal = (i + 1) * 2000
            total = sales + purchase + receipt + payment + journal
            
            data.append({
                'month': month,
                'sales': sales,
                'purchase': purchase,
                'receipt': receipt,
                'payment': payment,
                'journal': journal,
                'total': total
            })
        
        return data
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.summary_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            fy_str = self.fy_var.get()
            
            # Prepare data for export
            data = []
            headers = ['Month', 'Sales', 'Purchase', 'Receipt', 'Payment', 'Journal', 'Total']
            data.append(headers)
            
            for item in self.summary_tree.get_children():
                values = self.summary_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Yearly_Report_{fy_str}.xlsx"
            success, result = self.excel_exporter.export_yearly_report(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")