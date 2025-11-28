import sqlite3
from datetime import datetime, timedelta
from database import db_instance

class ReportController:
    def get_daily_report(self, date):
        """Get daily transaction report"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.voucher_type, v.voucher_number, v.voucher_date, 
                   l.name as party_name, v.total_amount, v.narration
            FROM vouchers v
            LEFT JOIN ledgers l ON v.party_ledger_id = l.id
            WHERE v.voucher_date = ?
            ORDER BY v.voucher_date, v.voucher_number
        ''', (date,))
        
        report_data = cursor.fetchall()
        conn.close()
        
        return report_data
    
    def get_monthly_report(self, year, month):
        """Get monthly report"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.voucher_type, COUNT(*) as count, SUM(v.total_amount) as total
            FROM vouchers v
            WHERE v.voucher_date BETWEEN ? AND ?
            GROUP BY v.voucher_type
        ''', (start_date, end_date))
        
        report_data = cursor.fetchall()
        conn.close()
        
        return report_data
    
    def get_profit_loss(self, start_date, end_date):
        """Get profit and loss statement"""
        # This would involve complex accounting calculations
        pass
    
    def get_balance_sheet(self, as_on_date):
        """Get balance sheet as on specific date"""
        # This would involve complex accounting calculations
        pass