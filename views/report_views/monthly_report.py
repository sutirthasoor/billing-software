import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import Config
from assets.styles.theme import theme
from controllers.report_controller import ReportController
from utils.printers import print_manager
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class MonthlyReportView:
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
        
        ttk.Label(header_frame, text="Monthly Summary Report", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="Select Month", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Month and Year Selection
        ttk.Label(filters_frame, text="Month:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.month_var = tk.StringVar(value=datetime.now().month)
        month_combo = ttk.Combobox(filters_frame, textvariable=self.month_var,
                                  values=list(range(1, 13)), style='Modern.TCombobox', width=10)
        month_combo.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        ttk.Label(filters_frame, text="Year:", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        current_year = datetime.now().year
        self.year_var = tk.StringVar(value=current_year)
        year_combo = ttk.Combobox(filters_frame, textvariable=self.year_var,
                                 values=list(range(current_year-5, current_year+1)), 
                                 style='Modern.TCombobox', width=10)
        year_combo.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Action Buttons
        action_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, columnspan=4, sticky='w', pady=15)
        
        ttk.Button(action_frame, text="Generate Report", style='Modern.TButton',
                  command=self.generate_report).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Export to Excel", style='Success.TButton',
                  command=self.export_to_excel).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Print Report", style='Secondary.TButton',
                  command=self.print_report).pack(side='left')
        
        # Summary Card
        self.summary_card = theme.create_card(container)
        self.summary_card.pack(fill='x', pady=(0, 10))
        
        self.summary_frame = ttk.Frame(self.summary_card, style='Modern.TFrame')
        self.summary_frame.pack(fill='x', padx=15, pady=15)
        
        # Initially hide summary
        self.summary_card.pack_forget()
        
        # Report Data Card
        data_card = theme.create_card(container)
        data_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(data_card, text="Monthly Voucher Summary", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Summary Table
        columns = ('voucher_type', 'count', 'total_amount')
        self.summary_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.summary_tree.heading('voucher_type', text='Voucher Type')
        self.summary_tree.heading('count', text='Count')
        self.summary_tree.heading('total_amount', text='Total Amount')
        
        self.summary_tree.column('voucher_type', width=200)
        self.summary_tree.column('count', width=100)
        self.summary_tree.column('total_amount', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        self.summary_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select month and year to generate monthly report")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def generate_report(self):
        """Generate monthly report"""
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            
            # Clear previous data
            for item in self.summary_tree.get_children():
                self.summary_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating monthly report...")
            self.parent.update()
            
            # Get monthly report data
            report_data = self.report_controller.get_monthly_report(year, month)
            
            if not report_data:
                month_name = Helpers.get_month_name(month)
                self.status_var.set(f"No transactions found for {month_name} {year}")
                self.summary_card.pack_forget()
                return
            
            # Calculate totals
            total_vouchers = sum(row[1] for row in report_data)
            total_amount = sum(row[2] for row in report_data)
            
            # Update summary
            self.update_summary(total_vouchers, total_amount, month, year)
            
            # Populate summary table
            for row in report_data:
                voucher_type, count, total = row
                self.summary_tree.insert('', 'end', values=(
                    voucher_type,
                    count,
                    f"{Config.CURRENCY} {total:,.2f}"
                ))
            
            month_name = Helpers.get_month_name(month)
            self.status_var.set(f"Monthly report generated for {month_name} {year}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def update_summary(self, total_vouchers, total_amount, month, year):
        """Update report summary"""
        # Clear previous summary
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        month_name = Helpers.get_month_name(month)
        
        # Create summary items
        summary_items = [
            ("Report Period:", f"{month_name} {year}"),
            ("Total Vouchers:", str(total_vouchers)),
            ("Total Amount:", f"{Config.CURRENCY} {total_amount:,.2f}")
        ]
        
        for i, (label, value) in enumerate(summary_items):
            ttk.Label(self.summary_frame, text=label, style='Normal.TLabel',
                     font=('Segoe UI', 9, 'bold')).grid(row=0, column=i*2, sticky='w', pady=5, padx=(0, 5))
            ttk.Label(self.summary_frame, text=value, style='Normal.TLabel').grid(row=0, column=i*2+1, sticky='w', pady=5, padx=(0, 20))
        
        # Show summary card
        self.summary_card.pack(fill='x', pady=(0, 10))
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.summary_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            month_name = Helpers.get_month_name(month)
            
            # Prepare data for export
            data = []
            headers = ['Voucher Type', 'Count', 'Total Amount']
            data.append(headers)
            
            for item in self.summary_tree.get_children():
                values = self.summary_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Monthly_Report_{month_name}_{year}.xlsx"
            success, result = self.excel_exporter.export_monthly_report(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def print_report(self):
        """Print the monthly report"""
        if not self.summary_tree.get_children():
            messagebox.showwarning("Warning", "No data to print. Please generate a report first.")
            return
        
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            month_name = Helpers.get_month_name(month)
            
            # Prepare report data
            report_data = []
            for item in self.summary_tree.get_children():
                values = self.summary_tree.item(item)['values']
                report_data.append(values)
            
            # Print using print manager
            # Note: You would need to implement print_monthly_report in print_manager
            messagebox.showinfo("Print", "Monthly report print functionality would be implemented here")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")