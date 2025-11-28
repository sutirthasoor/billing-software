import os
import json
from datetime import datetime, timedelta
from decimal import Decimal
from config import Config

class Helpers:
    @staticmethod
    def format_currency(amount):
        """Format amount as currency"""
        try:
            return f"{Config.CURRENCY} {float(amount):,.2f}"
        except (ValueError, TypeError):
            return f"{Config.CURRENCY} 0.00"
    
    @staticmethod
    def format_date(date_obj):
        """Format date object to string"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime(Config.DATE_FORMAT)
    
    @staticmethod
    def parse_date(date_str):
        """Parse date string to date object"""
        try:
            return datetime.strptime(date_str, Config.DATE_FORMAT).date()
        except ValueError:
            return datetime.now().date()
    
    @staticmethod
    def get_current_date():
        """Get current date as string"""
        return datetime.now().strftime(Config.DATE_FORMAT)
    
    @staticmethod
    def get_date_range(period='month'):
        """Get date range for different periods"""
        today = datetime.now().date()
        
        if period == 'today':
            start_date = today
            end_date = today
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == 'month':
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            start_date = today
            end_date = today
        
        return start_date, end_date
    
    @staticmethod
    def decimal_to_float(data):
        """Convert Decimal objects to float for JSON serialization"""
        if isinstance(data, dict):
            return {k: Helpers.decimal_to_float(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [Helpers.decimal_to_float(item) for item in data]
        elif isinstance(data, Decimal):
            return float(data)
        else:
            return data
    
    @staticmethod
    def generate_backup_filename():
        """Generate backup filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}.db"
    
    @staticmethod
    def calculate_tax(amount, tax_rate):
        """Calculate tax amount"""
        try:
            tax_amount = (float(amount) * float(tax_rate)) / 100
            return round(tax_amount, 2)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def get_financial_year(date=None):
        """Get financial year (April to March)"""
        if date is None:
            date = datetime.now()
        
        year = date.year
        if date.month < 4:  # January to March
            return f"{year-1}-{year}"
        else:  # April to December
            return f"{year}-{year+1}"