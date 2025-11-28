import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, mm
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from config import Config
from utils.constants import *

class PDFPrinter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for PDF"""
        self.styles.add(ParagraphStyle(
            name='CompanyTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            alignment=1
        ))
        
        self.styles.add(ParagraphStyle(
            name='NormalCenter',
            parent=self.styles['Normal'],
            alignment=1
        ))
    
    def create_voucher_pdf(self, voucher, output_path=None):
        """Create PDF for a voucher"""
        if not output_path:
            output_path = f"voucher_{voucher.voucher_number}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Company Header
        company_info = self.get_company_header()
        story.extend(company_info)
        
        # Voucher Header
        story.append(Paragraph("VOUCHER", self.styles['ReportTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Voucher Details Table
        voucher_data = [
            ["Voucher Type:", voucher.voucher_type],
            ["Voucher No:", voucher.voucher_number],
            ["Date:", voucher.voucher_date.strftime(Config.DATE_FORMAT)],
            ["Narration:", voucher.narration or ""]
        ]
        
        voucher_table = Table(voucher_data, colWidths=[1.5*inch, 4*inch])
        voucher_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(voucher_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Voucher Items Table
        items_data = [["Ledger", "Type", "Amount", "Narration"]]
        
        for item in voucher.items:
            items_data.append([
                self.get_ledger_name(item.ledger_id),
                item.type,
                f"{Config.CURRENCY} {item.amount:,.2f}",
                item.narration or ""
            ])
        
        items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1.8*inch])
        items_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Total Amount
        total_data = [["Total Amount:", f"{Config.CURRENCY} {voucher.total_amount:,.2f}"]]
        total_table = Table(total_data, colWidths=[4*inch, 2*inch])
        total_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 10),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ]))
        
        story.append(total_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 
                          self.styles['NormalCenter'])
        story.append(footer)
        
        try:
            doc.build(story)
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def create_ledger_pdf(self, ledger, transactions, start_date, end_date, output_path=None):
        """Create PDF for ledger report"""
        if not output_path:
            output_path = f"ledger_{ledger.name}_{start_date}_to_{end_date}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Company Header
        company_info = self.get_company_header()
        story.extend(company_info)
        
        # Report Title
        title = f"LEDGER REPORT - {ledger.name}"
        story.append(Paragraph(title, self.styles['ReportTitle']))
        
        # Period
        period = f"Period: {start_date} to {end_date}"
        story.append(Paragraph(period, self.styles['NormalCenter']))
        story.append(Spacer(1, 0.2*inch))
        
        # Opening Balance
        opening_balance = self.calculate_opening_balance(ledger, start_date)
        opening_data = [
            ["Opening Balance:", f"{Config.CURRENCY} {opening_balance:,.2f}"]
        ]
        opening_table = Table(opening_data, colWidths=[4*inch, 2*inch])
        opening_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 10),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ]))
        
        story.append(opening_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Transactions Table
        if transactions:
            trans_data = [["Date", "Voucher No", "Particulars", "Debit", "Credit", "Balance"]]
            
            running_balance = opening_balance
            
            for trans in transactions:
                date = trans[2].strftime(Config.DATE_FORMAT)
                voucher_no = trans[1]
                particulars = trans[5] or ""
                debit = trans[6] if trans[7] == 'Debit' else 0
                credit = trans[6] if trans[7] == 'Credit' else 0
                
                if ledger.balance_type == 'Debit':
                    running_balance += debit - credit
                else:
                    running_balance += credit - debit
                
                trans_data.append([
                    date,
                    voucher_no,
                    particulars,
                    f"{debit:,.2f}" if debit else "",
                    f"{credit:,.2f}" if credit else "",
                    f"{running_balance:,.2f}"
                ])
            
            trans_table = Table(trans_data, colWidths=[0.7*inch, 0.8*inch, 2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            trans_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (3, 0), (5, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 7),
            ]))
            
            story.append(trans_table)
            
            # Closing Balance
            closing_data = [
                ["Closing Balance:", f"{Config.CURRENCY} {running_balance:,.2f}"]
            ]
            closing_table = Table(closing_data, colWidths=[4*inch, 2*inch])
            closing_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 10),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ]))
            
            story.append(Spacer(1, 0.2*inch))
            story.append(closing_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 
                          self.styles['NormalCenter'])
        story.append(footer)
        
        try:
            doc.build(story)
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def create_daily_report_pdf(self, report_data, date, output_path=None):
        """Create PDF for daily report"""
        if not output_path:
            output_path = f"daily_report_{date}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=0.5*inch
        )
        
        story = []
        
        # Company Header
        company_info = self.get_company_header()
        story.extend(company_info)
        
        # Report Title
        title = f"DAILY TRANSACTION REPORT"
        story.append(Paragraph(title, self.styles['ReportTitle']))
        story.append(Paragraph(f"Date: {date}", self.styles['NormalCenter']))
        story.append(Spacer(1, 0.2*inch))
        
        if report_data:
            # Summary by voucher type
            summary_data = self.get_daily_summary(report_data)
            
            summary_table_data = [["Voucher Type", "Count", "Total Amount"]]
            for voucher_type, count, total in summary_data:
                summary_table_data.append([
                    voucher_type,
                    str(count),
                    f"{Config.CURRENCY} {total:,.2f}"
                ])
            
            summary_table = Table(summary_table_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Detailed transactions
            detailed_data = [["Type", "Voucher No", "Party", "Amount", "Narration"]]
            
            for row in report_data:
                detailed_data.append([
                    row[0],  # voucher_type
                    row[1],  # voucher_number
                    row[3] or "",  # party_name
                    f"{Config.CURRENCY} {row[4]:,.2f}",  # total_amount
                    row[5] or ""  # narration
                ])
            
            detailed_table = Table(detailed_data, colWidths=[1*inch, 1*inch, 1.5*inch, 1*inch, 1.5*inch])
            detailed_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 7),
            ]))
            
            story.append(detailed_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 
                          self.styles['NormalCenter'])
        story.append(footer)
        
        try:
            doc.build(story)
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def get_company_header(self):
        """Get company header for PDF"""
        from controllers.user_controller import UserController
        from models.company import Company
        
        # This would fetch company info from database
        # For now, using default
        company_name = Config.COMPANY_NAME
        
        header = []
        header.append(Paragraph(company_name, self.styles['CompanyTitle']))
        header.append(Spacer(1, 0.1*inch))
        return header
    
    def get_ledger_name(self, ledger_id):
        """Get ledger name by ID"""
        from controllers.ledger_controller import LedgerController
        
        controller = LedgerController()
        ledgers = controller.get_all_ledgers()
        
        for ledger in ledgers:
            if ledger.id == ledger_id:
                return ledger.name
        
        return "Unknown Ledger"
    
    def calculate_opening_balance(self, ledger, start_date):
        """Calculate opening balance for ledger"""
        # This would involve querying transactions before start_date
        # For now, return the opening balance
        return float(ledger.opening_balance)
    
    def get_daily_summary(self, report_data):
        """Get daily summary by voucher type"""
        summary = {}
        
        for row in report_data:
            voucher_type = row[0]
            amount = row[4]
            
            if voucher_type not in summary:
                summary[voucher_type] = {'count': 0, 'total': 0}
            
            summary[voucher_type]['count'] += 1
            summary[voucher_type]['total'] += amount
        
        result = []
        for voucher_type, data in summary.items():
            result.append((voucher_type, data['count'], data['total']))
        
        return result

class PrintManager:
    def __init__(self):
        self.pdf_printer = PDFPrinter()
    
    def print_voucher(self, voucher):
        """Print voucher"""
        success, result = self.pdf_printer.create_voucher_pdf(voucher)
        
        if success:
            self.show_print_dialog(result, f"Voucher {voucher.voucher_number}")
        else:
            messagebox.showerror("Print Error", f"Failed to create PDF: {result}")
    
    def print_ledger_report(self, ledger, transactions, start_date, end_date):
        """Print ledger report"""
        success, result = self.pdf_printer.create_ledger_pdf(ledger, transactions, start_date, end_date)
        
        if success:
            self.show_print_dialog(result, f"Ledger Report - {ledger.name}")
        else:
            messagebox.showerror("Print Error", f"Failed to create PDF: {result}")
    
    def print_daily_report(self, report_data, date):
        """Print daily report"""
        success, result = self.pdf_printer.create_daily_report_pdf(report_data, date)
        
        if success:
            self.show_print_dialog(result, f"Daily Report - {date}")
        else:
            messagebox.showerror("Print Error", f"Failed to create PDF: {result}")
    
    def show_print_dialog(self, file_path, title):
        """Show print dialog"""
        try:
            # On Windows
            os.startfile(file_path, "print")
            messagebox.showinfo("Print", f"{title} sent to printer")
        except:
            # On other platforms or if os.startfile fails
            messagebox.showinfo("Print", 
                              f"{title} saved as PDF:\n{file_path}\n\nPlease open and print manually.")

# Global printer instance
print_manager = PrintManager()