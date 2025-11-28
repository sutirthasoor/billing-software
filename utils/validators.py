import re
from datetime import datetime
from config import Config

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) if email else True
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (10 digits)"""
        pattern = r'^\d{10}$'
        return bool(re.match(pattern, phone)) if phone else True
    
    @staticmethod
    def validate_gstin(gstin):
        """Validate GSTIN format"""
        if not gstin:
            return True
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        return bool(re.match(pattern, gstin.upper()))
    
    @staticmethod
    def validate_date(date_str):
        """Validate date string"""
        try:
            datetime.strptime(date_str, Config.DATE_FORMAT)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_amount(amount):
        """Validate amount (positive number)"""
        try:
            amount_float = float(amount)
            return amount_float >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_required(value):
        """Check if value is not empty"""
        return bool(str(value).strip()) if value is not None else False
    
    @staticmethod
    def validate_hsn_code(hsn):
        """Validate HSN code (4-8 digits)"""
        if not hsn:
            return True
        pattern = r'^\d{4,8}$'
        return bool(re.match(pattern, hsn))
    
    @staticmethod
    def validate_percentage(percentage):
        """Validate percentage (0-100)"""
        try:
            perc_float = float(percentage)
            return 0 <= perc_float <= 100
        except (ValueError, TypeError):
            return False