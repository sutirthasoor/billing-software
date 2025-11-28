import sqlite3
from models.voucher import Voucher, VoucherItem
from database import db_instance
from datetime import datetime

class VoucherController:
    def create_voucher(self, voucher_data):
        """Create a new voucher"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insert voucher
            cursor.execute('''
                INSERT INTO vouchers (voucher_type, voucher_number, voucher_date, 
                                   party_ledger_id, narration, total_amount, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                voucher_data['voucher_type'],
                voucher_data['voucher_number'],
                voucher_data['voucher_date'],
                voucher_data['party_ledger_id'],
                voucher_data['narration'],
                voucher_data['total_amount'],
                voucher_data['created_by']
            ))
            
            voucher_id = cursor.lastrowid
            
            # Insert voucher items
            for item in voucher_data['items']:
                cursor.execute('''
                    INSERT INTO voucher_items (voucher_id, ledger_id, amount, type, narration)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    voucher_id,
                    item['ledger_id'],
                    item['amount'],
                    item['type'],
                    item['narration']
                ))
            
            # Update voucher type next number
            cursor.execute('''
                UPDATE voucher_types SET next_number = next_number + 1 WHERE name = ?
            ''', (voucher_data['voucher_type'],))
            
            conn.commit()
            conn.close()
            return voucher_id
            
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def get_voucher_by_number(self, voucher_number):
        """Get voucher by number"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vouchers WHERE voucher_number = ?', (voucher_number,))
        voucher_data = cursor.fetchone()
        
        if voucher_data:
            # Get voucher items
            cursor.execute('SELECT * FROM voucher_items WHERE voucher_id = ?', (voucher_data[0],))
            items_data = cursor.fetchall()
            
            items = [VoucherItem(*item) for item in items_data]
            voucher = Voucher(*voucher_data)
            voucher.items = items
            
            conn.close()
            return voucher
        
        conn.close()
        return None
    
    def get_vouchers_by_date_range(self, start_date, end_date, voucher_type=None):
        """Get vouchers by date range"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        if voucher_type:
            cursor.execute('''
                SELECT * FROM vouchers 
                WHERE voucher_date BETWEEN ? AND ? AND voucher_type = ?
                ORDER BY voucher_date DESC, voucher_number DESC
            ''', (start_date, end_date, voucher_type))
        else:
            cursor.execute('''
                SELECT * FROM vouchers 
                WHERE voucher_date BETWEEN ? AND ?
                ORDER BY voucher_date DESC, voucher_number DESC
            ''', (start_date, end_date))
        
        vouchers_data = cursor.fetchall()
        vouchers = []
        
        for voucher_data in vouchers_data:
            voucher = Voucher(*voucher_data)
            vouchers.append(voucher)
        
        conn.close()
        return vouchers
    
    def get_next_voucher_number(self, voucher_type):
        """Get next voucher number for a type"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT prefix, next_number FROM voucher_types WHERE name = ?', (voucher_type,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            prefix, next_number = result
            return f"{prefix}/{next_number:04d}"
        return None