import csv
import json
import pandas as pd
from datetime import datetime
from config import Config

class Exporters:
    @staticmethod
    def export_to_csv(data, filename, headers=None):
        """Export data to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                if headers:
                    writer.writerow(headers)
                
                for row in data:
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    @staticmethod
    def export_to_excel(data, filename, sheet_name='Data', headers=None):
        """Export data to Excel file"""
        try:
            df = pd.DataFrame(data)
            if headers and len(headers) == len(df.columns):
                df.columns = headers
            
            df.to_excel(filename, sheet_name=sheet_name, index=False)
            return True
        except Exception as e:
            print(f"Excel export error: {e}")
            return False
    
    @staticmethod
    def export_to_json(data, filename):
        """Export data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, default=str)
            return True
        except Exception as e:
            print(f"JSON export error: {e}")
            return False
    
    @staticmethod
    def export_vouchers(vouchers, filename, format_type='csv'):
        """Export vouchers data"""
        data = []
        headers = ['Voucher Type', 'Number', 'Date', 'Party', 'Amount', 'Narration']
        
        for voucher in vouchers:
            data.append([
                voucher.voucher_type,
                voucher.voucher_number,
                voucher.voucher_date,
                voucher.party_ledger_id,  # Would need to resolve ledger name
                voucher.total_amount,
                voucher.narration or ''
            ])
        
        if format_type.lower() == 'csv':
            return Exporters.export_to_csv(data, filename, headers)
        elif format_type.lower() == 'excel':
            return Exporters.export_to_excel(data, filename, 'Vouchers', headers)
        elif format_type.lower() == 'json':
            return Exporters.export_to_json([v.to_dict() for v in vouchers], filename)
        
        return False
    
    @staticmethod
    def export_ledgers(ledgers, filename, format_type='csv'):
        """Export ledgers data"""
        data = []
        headers = ['Name', 'Group', 'Opening Balance', 'Balance Type', 'Contact', 'Phone']
        
        for ledger in ledgers:
            data.append([
                ledger.name,
                ledger.group_id,  # Would need to resolve group name
                ledger.opening_balance,
                ledger.balance_type,
                ledger.contact_person or '',
                ledger.phone or ''
            ])
        
        if format_type.lower() == 'csv':
            return Exporters.export_to_csv(data, filename, headers)
        elif format_type.lower() == 'excel':
            return Exporters.export_to_excel(data, filename, 'Ledgers', headers)
        
        return False