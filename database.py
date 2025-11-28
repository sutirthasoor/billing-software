import sqlite3
import os
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                last_login TIMESTAMP
            )
        ''')
        
        # Company table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                gstin TEXT,
                state TEXT,
                state_code TEXT,
                logo_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ledger Groups
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                parent_id INTEGER,
                type TEXT CHECK(type IN ('Income', 'Expense', 'Asset', 'Liability', 'Capital')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ledgers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledgers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER,
                opening_balance DECIMAL(15,2) DEFAULT 0,
                balance_type TEXT CHECK(balance_type IN ('Debit', 'Credit')),
                contact_person TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                gstin TEXT,
                state TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES ledger_groups (id)
            )
        ''')
        
        # Voucher Types
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                prefix TEXT,
                next_number INTEGER DEFAULT 1,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Vouchers Master
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_type TEXT NOT NULL,
                voucher_number TEXT UNIQUE NOT NULL,
                voucher_date DATE NOT NULL,
                party_ledger_id INTEGER,
                narration TEXT,
                total_amount DECIMAL(15,2) DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (party_ledger_id) REFERENCES ledgers (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Voucher Items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_id INTEGER,
                ledger_id INTEGER,
                amount DECIMAL(15,2) NOT NULL,
                type TEXT CHECK(type IN ('Debit', 'Credit')) NOT NULL,
                narration TEXT,
                FOREIGN KEY (voucher_id) REFERENCES vouchers (id) ON DELETE CASCADE,
                FOREIGN KEY (ledger_id) REFERENCES ledgers (id)
            )
        ''')
        
        # Inventory Items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE,
                unit TEXT,
                hsn_code TEXT,
                tax_rate DECIMAL(5,2) DEFAULT 0,
                purchase_rate DECIMAL(10,2) DEFAULT 0,
                sales_rate DECIMAL(10,2) DEFAULT 0,
                current_stock DECIMAL(10,2) DEFAULT 0,
                min_stock DECIMAL(10,2) DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # System Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                module TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default data
        self.insert_default_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_default_data(self, cursor):
        # Insert default user
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, full_name, email, role) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin123', 'Administrator', 'admin@company.com', 'admin'))
        
        # Insert default company
        cursor.execute('''
            INSERT OR IGNORE INTO company (name, address, phone, email) 
            VALUES (?, ?, ?, ?)
        ''', ('Your Company Name', 'Company Address', '1234567890', 'info@company.com'))
        
        # Insert default ledger groups
        groups = [
            ('Capital Account', None, 'Capital'),
            ('Current Assets', None, 'Asset'),
            ('Fixed Assets', None, 'Asset'),
            ('Investments', None, 'Asset'),
            ('Current Liabilities', None, 'Liability'),
            ('Loans', None, 'Liability'),
            ('Sales Accounts', None, 'Income'),
            ('Purchase Accounts', None, 'Expense'),
            ('Direct Incomes', None, 'Income'),
            ('Indirect Incomes', None, 'Income'),
            ('Direct Expenses', None, 'Expense'),
            ('Indirect Expenses', None, 'Expense')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO ledger_groups (name, parent_id, type) 
            VALUES (?, ?, ?)
        ''', groups)
        
        # Insert default voucher types
        voucher_types = [
            ('Sales', 'SL', 1),
            ('Purchase', 'PR', 1),
            ('Receipt', 'RCP', 1),
            ('Payment', 'PAY', 1),
            ('Journal', 'JNL', 1),
            ('Contra', 'CTR', 1)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO voucher_types (name, prefix, next_number) 
            VALUES (?, ?, ?)
        ''', voucher_types)

# Singleton instance
db_instance = Database()
import os
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                last_login TIMESTAMP
            )
        ''')
        
        # Company table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                gstin TEXT,
                state TEXT,
                state_code TEXT,
                logo_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ledger Groups
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                parent_id INTEGER,
                type TEXT CHECK(type IN ('Income', 'Expense', 'Asset', 'Liability', 'Capital')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ledgers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledgers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER,
                opening_balance DECIMAL(15,2) DEFAULT 0,
                balance_type TEXT CHECK(balance_type IN ('Debit', 'Credit')),
                contact_person TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                gstin TEXT,
                state TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES ledger_groups (id)
            )
        ''')
        
        # Voucher Types
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                prefix TEXT,
                next_number INTEGER DEFAULT 1,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Vouchers Master
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_type TEXT NOT NULL,
                voucher_number TEXT UNIQUE NOT NULL,
                voucher_date DATE NOT NULL,
                party_ledger_id INTEGER,
                narration TEXT,
                total_amount DECIMAL(15,2) DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (party_ledger_id) REFERENCES ledgers (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Voucher Items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_id INTEGER,
                ledger_id INTEGER,
                amount DECIMAL(15,2) NOT NULL,
                type TEXT CHECK(type IN ('Debit', 'Credit')) NOT NULL,
                narration TEXT,
                FOREIGN KEY (voucher_id) REFERENCES vouchers (id) ON DELETE CASCADE,
                FOREIGN KEY (ledger_id) REFERENCES ledgers (id)
            )
        ''')
        
        # Inventory Items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE,
                unit TEXT,
                hsn_code TEXT,
                tax_rate DECIMAL(5,2) DEFAULT 0,
                purchase_rate DECIMAL(10,2) DEFAULT 0,
                sales_rate DECIMAL(10,2) DEFAULT 0,
                current_stock DECIMAL(10,2) DEFAULT 0,
                min_stock DECIMAL(10,2) DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # System Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                module TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default data
        self.insert_default_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_default_data(self, cursor):
        # Insert default user
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, full_name, email, role) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin123', 'Administrator', 'admin@company.com', 'admin'))
        
        # Insert default company
        cursor.execute('''
            INSERT OR IGNORE INTO company (name, address, phone, email) 
            VALUES (?, ?, ?, ?)
        ''', ('Your Company Name', 'Company Address', '1234567890', 'info@company.com'))
        
        # Insert default ledger groups
        groups = [
            ('Capital Account', None, 'Capital'),
            ('Current Assets', None, 'Asset'),
            ('Fixed Assets', None, 'Asset'),
            ('Investments', None, 'Asset'),
            ('Current Liabilities', None, 'Liability'),
            ('Loans', None, 'Liability'),
            ('Sales Accounts', None, 'Income'),
            ('Purchase Accounts', None, 'Expense'),
            ('Direct Incomes', None, 'Income'),
            ('Indirect Incomes', None, 'Income'),
            ('Direct Expenses', None, 'Expense'),
            ('Indirect Expenses', None, 'Expense')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO ledger_groups (name, parent_id, type) 
            VALUES (?, ?, ?)
        ''', groups)
        
        # Insert default voucher types
        voucher_types = [
            ('Sales', 'SL', 1),
            ('Purchase', 'PR', 1),
            ('Receipt', 'RCP', 1),
            ('Payment', 'PAY', 1),
            ('Journal', 'JNL', 1),
            ('Contra', 'CTR', 1)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO voucher_types (name, prefix, next_number) 
            VALUES (?, ?, ?)
        ''', voucher_types)

# Singleton instance
db_instance = Database()