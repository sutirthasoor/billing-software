import sqlite3
from models.inventory import InventoryItem
from database import db_instance

class InventoryController:
    def create_item(self, item_data):
        """Create new inventory item"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO inventory_items (name, code, unit, hsn_code, tax_rate,
                                          purchase_rate, sales_rate, current_stock, min_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item_data['name'],
                item_data['code'],
                item_data['unit'],
                item_data['hsn_code'],
                item_data['tax_rate'],
                item_data['purchase_rate'],
                item_data['sales_rate'],
                item_data['current_stock'],
                item_data['min_stock']
            ))
            
            item_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return item_id
            
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_all_items(self):
        """Get all inventory items"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM inventory_items WHERE is_active = 1 ORDER BY name')
        items_data = cursor.fetchall()
        conn.close()
        
        return [InventoryItem(*data) for data in items_data]
    
    def update_stock(self, item_id, quantity):
        """Update item stock"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE inventory_items 
            SET current_stock = current_stock + ? 
            WHERE id = ?
        ''', (quantity, item_id))
        
        conn.commit()
        conn.close()
        return True