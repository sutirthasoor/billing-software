from datetime import datetime

class Company:
    def __init__(self, company_id=None, name="", address="", phone="", email="", 
                 gstin="", state="", state_code="", logo_path="", created_at=None):
        self.id = company_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.gstin = gstin
        self.state = state
        self.state_code = state_code
        self.logo_path = logo_path
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'gstin': self.gstin,
            'state': self.state,
            'state_code': self.state_code,
            'logo_path': self.logo_path,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            company_id=data.get('id'),
            name=data.get('name', ''),
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            gstin=data.get('gstin', ''),
            state=data.get('state', ''),
            state_code=data.get('state_code', ''),
            logo_path=data.get('logo_path', ''),
            created_at=data.get('created_at')
        )