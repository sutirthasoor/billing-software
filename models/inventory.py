from datetime import datetime
from decimal import Decimal

class InventoryItem:
    def __init__(self, item_id=None, name="", code="", unit="", hsn_code="", tax_rate=Decimal('0'),
                 purchase_rate=Decimal('0'), sales_rate=Decimal('0'), current_stock=Decimal('0'),
                 min_stock=Decimal('0'), is_active=True, created_at=None):
        self.id = item_id
        self.name = name
        self.code = code
        self.unit = unit
        self.hsn_code = hsn_code
        self.tax_rate = tax_rate
        self.purchase_rate = purchase_rate
        self.sales_rate = sales_rate
        self.current_stock = current_stock
        self.min_stock = min_stock
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'unit': self.unit,
            'hsn_code': self.hsn_code,
            'tax_rate': float(self.tax_rate),
            'purchase_rate': float(self.purchase_rate),
            'sales_rate': float(self.sales_rate),
            'current_stock': float(self.current_stock),
            'min_stock': float(self.min_stock),
            'is_active': self.is_active,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data.get('id'),
            name=data.get('name', ''),
            code=data.get('code', ''),
            unit=data.get('unit', ''),
            hsn_code=data.get('hsn_code', ''),
            tax_rate=Decimal(str(data.get('tax_rate', 0))),
            purchase_rate=Decimal(str(data.get('purchase_rate', 0))),
            sales_rate=Decimal(str(data.get('sales_rate', 0))),
            current_stock=Decimal(str(data.get('current_stock', 0))),
            min_stock=Decimal(str(data.get('min_stock', 0))),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at')
        )