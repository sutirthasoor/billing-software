import os
from datetime import datetime

class Config:
    # App Configuration
    APP_NAME = "Modern Billing Software"
    VERSION = "1.0.0"
    COMPANY_NAME = "Your Company Name"
    
    # Database Configuration
    DATABASE_PATH = "billing_software.db"
    BACKUP_PATH = "backups/"
    
    # UI Configuration - WHITE THEME
    THEME = {
        'primary': '#FFFFFF',  # Pure White
        'secondary': '#F8F9FA',  # Light Gray
        'accent': '#007ACC',  # Blue Accent
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545',
        'text_primary': '#2C3E50',
        'text_secondary': '#6C757D',
        'border': '#E9ECEF',
        'hover': '#E3F2FD'
    }
    
    # Font Configuration
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'normal': ('Segoe UI', 11),
        'small': ('Segoe UI', 10)
    }
    
    # Window Sizes
    MAIN_WINDOW_SIZE = "1400x900"
    LOGIN_WINDOW_SIZE = "400x500"
    
    # Business Configuration
    CURRENCY = "₹"
    DATE_FORMAT = "%d-%m-%Y"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.BACKUP_PATH, exist_ok=True)