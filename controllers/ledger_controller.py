import sqlite3
from models.ledger import Ledger, LedgerGroup
from database import db_instance

class LedgerController:
    def create_ledger(self, ledger_data):
        """Create new ledger"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO ledgers (name, group_id, opening_balance, balance_type,
                                  contact_person, address, phone, email, gstin, state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ledger_data['name'],
                ledger_data['group_id'],
                ledger_data['opening_balance'],
                ledger_data['balance_type'],
                ledger_data['contact_person'],
                ledger_data['address'],
                ledger_data['phone'],
                ledger_data['email'],
                ledger_data['gstin'],
                ledger_data['state']
            ))
            
            ledger_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return ledger_id
            
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_all_ledgers(self):
        """Get all ledgers"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT l.*, lg.name as group_name 
            FROM ledgers l 
            LEFT JOIN ledger_groups lg ON l.group_id = lg.id 
            WHERE l.is_active = 1
            ORDER BY l.name
        ''')
        
        ledgers_data = cursor.fetchall()
        conn.close()
        
        ledgers = []
        for data in ledgers_data:
            ledger = Ledger(*data[:12])  # First 12 fields are from ledgers table
            ledger.group_name = data[12]  # Group name from join
            ledgers.append(ledger)
        
        return ledgers
    
    def get_ledger_groups(self):
        """Get all ledger groups"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ledger_groups ORDER BY name')
        groups_data = cursor.fetchall()
        conn.close()
        
        return [LedgerGroup(*data) for data in groups_data]
    
    def get_ledger_balance(self, ledger_id, as_on_date=None):
        """Get ledger balance as on specific date"""
        # This would calculate opening balance + all transactions
        # Implementation would involve complex SQL query
        pass