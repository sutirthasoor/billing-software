import sqlite3
from models.user import User
from database import db_instance
from datetime import datetime

class UserController:
    def authenticate(self, username, password):
        """Authenticate user"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1
        ''', (username, password))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            # Update last login
            self.update_last_login(user_data[0])
            return User(*user_data)
        return None
    
    def update_last_login(self, user_id):
        """Update user's last login timestamp"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_login = ? WHERE id = ?
        ''', (datetime.now(), user_id))
        
        conn.commit()
        conn.close()
    
    def get_all_users(self):
        """Get all users"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users_data = cursor.fetchall()
        conn.close()
        
        return [User(*data) for data in users_data]
    
    def create_user(self, user_data):
        """Create new user"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, full_name, email, role, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_data['username'],
                user_data['password'],
                user_data['full_name'],
                user_data['email'],
                user_data['role'],
                user_data['phone']
            ))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def update_user(self, user_id, user_data):
        """Update user"""
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET username=?, full_name=?, email=?, role=?, phone=?, is_active=?
            WHERE id=?
        ''', (
            user_data['username'],
            user_data['full_name'],
            user_data['email'],
            user_data['role'],
            user_data['phone'],
            user_data['is_active'],
            user_id
        ))
        
        conn.commit()
        conn.close()
        return True