from datetime import datetime

class User:
    def __init__(self, user_id=None, username="", password="", full_name="", email="", 
                 role="user", phone="", created_at=None, is_active=True, last_login=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
        self.phone = phone
        self.created_at = created_at or datetime.now()
        self.is_active = is_active
        self.last_login = last_login
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get('id'),
            username=data.get('username', ''),
            password=data.get('password', ''),
            full_name=data.get('full_name', ''),
            email=data.get('email', ''),
            role=data.get('role', 'user'),
            phone=data.get('phone', ''),
            created_at=data.get('created_at'),
            is_active=data.get('is_active', True),
            last_login=data.get('last_login')
        )