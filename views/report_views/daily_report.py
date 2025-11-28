import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from config import Config
from assets.styles.theme import theme
from controllers.report_controller import ReportController
from controllers.voucher_controller import VoucherController
from utils.printers import print_manager
from utils.exporters import ExcelExporter
from utils.helpers import Helpers

class DailyReportView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.report_controller = ReportController()
        self.voucher_controller = VoucherController()
        self.excel_exporter = ExcelExporter()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Daily Transaction Report", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Filters Card
        filters_card = theme.create_card(container)
        filters_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filters_card, text="Report Date", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        filters_frame = ttk.Frame(filters_card, style='Modern.TFrame')
        filters_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Date Selection
        ttk.Label(filters_frame, text="Select Date:", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.date_var = tk.StringVar(value=datetime.now().strftime(Config.DATE_FORMAT))
        self.date_entry = ttk.Entry(filters_frame, textvariable=self.date_var,
                                   style='Modern.TEntry', width=15)
        self.date_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Quick date buttons
        quick_dates_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        quick_dates_frame.grid(row=0, column=2, sticky='w', pady=8)
        
        ttk.Button(quick_dates_frame, text="Today", style='Secondary.TButton',
                  command=lambda: self.set_date(datetime.now())).pack(side='left', padx=(0, 5))
        ttk.Button(quick_dates_frame, text="Yesterday", style='Secondary.TButton',
                  command=lambda: self.set_date(datetime.now() - timedelta(days=1))).pack(side='left', padx=(0, 5))
        
        # Action Buttons
        action_frame = ttk.Frame(filters_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, columnspan=3, sticky='w', pady=15)
        
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
        
        ttk.Label(data_card, text="Daily Transactions", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Transactions Table
        columns = ('voucher_type', 'voucher_no', 'date', 'party', 'amount', 'narration')
        self.transactions_tree = ttk.Treeview(data_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.transactions_tree.heading('voucher_type', text='Type')
        self.transactions_tree.heading('voucher_no', text='Voucher No')
        self.transactions_tree.heading('date', text='Date')
        self.transactions_tree.heading('party', text='Party')
        self.transactions_tree.heading('amount', text='Amount')
        self.transactions_tree.heading('narration', text='Narration')
        
        self.transactions_tree.column('voucher_type', width=100)
        self.transactions_tree.column('voucher_no', width=120)
        self.transactions_tree.column('date', width=100)
        self.transactions_tree.column('party', width=150)
        self.transactions_tree.column('amount', width=120)
        self.transactions_tree.column('narration', width=200)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(data_card, orient='vertical', command=self.transactions_tree.yview)
        h_scrollbar = ttk.Scrollbar(data_card, orient='horizontal', command=self.transactions_tree.xview)
        self.transactions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.transactions_tree.pack(side='top', fill='both', expand=True, padx=15, pady=(0, 5))
        v_scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 5))
        h_scrollbar.pack(side='bottom', fill='x', padx=15, pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar(value="Select a date to generate daily report")
        status_bar = ttk.Frame(container, style='Modern.TFrame')
        status_bar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(status_bar, textvariable=self.status_var, style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).pack(side='left', padx=10, pady=5)
    
    def set_date(self, date_obj):
        """Set date in the date entry"""
        self.date_var.set(date_obj.strftime(Config.DATE_FORMAT))
    
    def validate_date(self):
        """Validate date input"""
        date_str = self.date_var.get().strip()
        
        if not date_str:
            messagebox.showerror("Error", "Please select a date")
            return False
        
        try:
            Helpers.parse_date(date_str)
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY")
            return False
    
    def generate_report(self):
        """Generate daily report"""
        if not self.validate_date():
            return
        
        try:
            date_str = self.date_var.get().strip()
            date_obj = Helpers.parse_date(date_str)
            
            # Clear previous data
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)
            
            # Show loading message
            self.status_var.set("Generating daily report...")
            self.parent.update()
            
            # Get daily report data
            report_data = self.report_controller.get_daily_report(date_obj)
            
            if not report_data:
                self.status_var.set(f"No transactions found for {date_str}")
                self.summary_card.pack_forget()
                return
            
            # Calculate summary
            summary = self.calculate_summary(report_data)
            
            # Update summary
            self.update_summary(summary, date_str)
            
            # Populate transactions table
            for row in report_data:
                voucher_type, voucher_no, date, party, amount, narration = row
                self.transactions_tree.insert('', 'end', values=(
                    voucher_type,
                    voucher_no,
                    date.strftime(Config.DATE_FORMAT) if hasattr(date, 'strftime') else date,
                    party or "",
                    f"{Config.CURRENCY} {amount:,.2f}",
                    narration or ""
                ))
            
            self.status_var.set(f"Daily report generated for {date_str} - {len(report_data)} transactions found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating report")
    
    def calculate_summary(self, report_data):
        """Calculate summary statistics"""
        summary = {
            'total_transactions': len(report_data),
            'total_amount': sum(row[4] for row in report_data),
            'voucher_counts': {},
            'voucher_totals': {}
        }
        
        for row in report_data:
            voucher_type = row[0]
            amount = row[4]
            
            if voucher_type not in summary['voucher_counts']:
                summary['voucher_counts'][voucher_type] = 0
                summary['voucher_totals'][voucher_type] = 0
            
            summary['voucher_counts'][voucher_type] += 1
            summary['voucher_totals'][voucher_type] += amount
        
        return summary
    
    def update_summary(self, summary, date_str):
        """Update report summary"""
        # Clear previous summary
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Create summary items
        summary_items = [
            ("Report Date:", date_str),
            ("Total Transactions:", str(summary['total_transactions'])),
            ("Total Amount:", f"{Config.CURRENCY} {summary['total_amount']:,.2f}")
        ]
        
        # Add voucher type breakdown
        row = 0
        for i, (label, value) in enumerate(summary_items):
            ttk.Label(self.summary_frame, text=label, style='Normal.TLabel',
                     font=('Segoe UI', 9, 'bold')).grid(row=row, column=i*2, sticky='w', pady=5, padx=(0, 5))
            ttk.Label(self.summary_frame, text=value, style='Normal.TLabel').grid(row=row, column=i*2+1, sticky='w', pady=5, padx=(0, 20))
        
        row += 1
        ttk.Label(self.summary_frame, text="Voucher Summary:", style='Heading.TLabel').grid(
            row=row, column=0, columnspan=6, sticky='w', pady=(10, 5))
        
        row += 1
        col = 0
        for voucher_type, count in summary['voucher_counts'].items():
            if col >= 6:  # Start new row after 3 items
                row += 1
                col = 0
            
            amount = summary['voucher_totals'][voucher_type]
            ttk.Label(self.summary_frame, text=f"{voucher_type}:", style='Small.TLabel',
                     font=('Segoe UI', 8, 'bold')).grid(row=row, column=col, sticky='w', pady=2, padx=(0, 5))
            ttk.Label(self.summary_frame, text=f"{count} vouchers, {Config.CURRENCY} {amount:,.2f}", 
                     style='Small.TLabel').grid(row=row, column=col+1, sticky='w', pady=2, padx=(0, 20))
            col += 2
        
        # Show summary card
        self.summary_card.pack(fill='x', pady=(0, 10))
    
    def export_to_excel(self):
        """Export report to Excel"""
        if not self.transactions_tree.get_children():
            messagebox.showwarning("Warning", "No data to export. Please generate a report first.")
            return
        
        try:
            date_str = self.date_var.get().strip()
            
            # Prepare data for export
            data = []
            headers = ['Voucher Type', 'Voucher No', 'Date', 'Party', 'Amount', 'Narration']
            data.append(headers)
            
            for item in self.transactions_tree.get_children():
                values = self.transactions_tree.item(item)['values']
                data.append(values)
            
            # Export to Excel
            filename = f"Daily_Report_{date_str}.xlsx"
            success, result = self.excel_exporter.export_daily_report(data, filename)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{result}")
            else:
                messagebox.showerror("Error", f"Failed to export: {result}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def print_report(self):
        """Print the daily report"""
        if not self.transactions_tree.get_children():
            messagebox.showwarning("Warning", "No data to print. Please generate a report first.")
            return
        
        try:
            date_str = self.date_var.get().strip()
            
            # Prepare report data
            report_data = []
            for item in self.transactions_tree.get_children():
                values = self.transactions_tree.item(item)['values']
                report_data.append(values)
            
            # Print using print manager
            print_manager.print_daily_report(report_data, date_str)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")