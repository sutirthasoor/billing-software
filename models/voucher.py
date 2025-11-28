from datetime import datetime
from decimal import Decimal

class VoucherType:
    def __init__(self, type_id=None, name="", prefix="", next_number=1, is_active=True):
        self.id = type_id
        self.name = name
        self.prefix = prefix
        self.next_number = next_number
        self.is_active = is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'prefix': self.prefix,
            'next_number': self.next_number,
            'is_active': self.is_active
        }

class VoucherItem:
    def __init__(self, item_id=None, voucher_id=None, ledger_id=None, amount=Decimal('0'), 
                 item_type="Debit", narration=""):
        self.id = item_id
        self.voucher_id = voucher_id
        self.ledger_id = ledger_id
        self.amount = amount
        self.type = item_type  # Debit or Credit
        self.narration = narration
    
    def to_dict(self):
        return {
            'id': self.id,
            'voucher_id': self.voucher_id,
            'ledger_id': self.ledger_id,
            'amount': float(self.amount),
            'type': self.type,
            'narration': self.narration
        }

class Voucher:
    def __init__(self, voucher_id=None, voucher_type="", voucher_number="", voucher_date=None,
                 party_ledger_id=None, narration="", total_amount=Decimal('0'), created_by=None, 
                 created_at=None, items=None):
        self.id = voucher_id
        self.voucher_type = voucher_type
        self.voucher_number = voucher_number
        self.voucher_date = voucher_date or datetime.now().date()
        self.party_ledger_id = party_ledger_id
        self.narration = narration
        self.total_amount = total_amount
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.items = items or []
    
    def to_dict(self):
        return {
            'id': self.id,
            'voucher_type': self.voucher_type,
            'voucher_number': self.voucher_number,
            'voucher_date': self.voucher_date,
            'party_ledger_id': self.party_ledger_id,
            'narration': self.narration,
            'total_amount': float(self.total_amount),
            'created_by': self.created_by,
            'created_at': self.created_at,
            'items': [item.to_dict() for item in self.items]
        }
    
    def add_item(self, item):
        self.items.append(item)
    
    def calculate_total(self):
        self.total_amount = sum(item.amount for item in self.items)