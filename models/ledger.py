from datetime import datetime
from decimal import Decimal

class LedgerGroup:
    def __init__(self, group_id=None, name="", parent_id=None, group_type="", created_at=None):
        self.id = group_id
        self.name = name
        self.parent_id = parent_id
        self.type = group_type  # Income, Expense, Asset, Liability, Capital
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'type': self.type,
            'created_at': self.created_at
        }

class Ledger:
    def __init__(self, ledger_id=None, name="", group_id=None, opening_balance=Decimal('0'), 
                 balance_type="Debit", contact_person="", address="", phone="", email="", 
                 gstin="", state="", is_active=True, created_at=None):
        self.id = ledger_id
        self.name = name
        self.group_id = group_id
        self.opening_balance = opening_balance
        self.balance_type = balance_type  # Debit or Credit
        self.contact_person = contact_person
        self.address = address
        self.phone = phone
        self.email = email
        self.gstin = gstin
        self.state = state
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'opening_balance': float(self.opening_balance),
            'balance_type': self.balance_type,
            'contact_person': self.contact_person,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'gstin': self.gstin,
            'state': self.state,
            'is_active': self.is_active,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            ledger_id=data.get('id'),
            name=data.get('name', ''),
            group_id=data.get('group_id'),
            opening_balance=Decimal(str(data.get('opening_balance', 0))),
            balance_type=data.get('balance_type', 'Debit'),
            contact_person=data.get('contact_person', ''),
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            gstin=data.get('gstin', ''),
            state=data.get('state', ''),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at')
        )