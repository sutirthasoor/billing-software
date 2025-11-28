# Application Constants

class VoucherTypes:
    SALES = "Sales"
    PURCHASE = "Purchase" 
    RECEIPT = "Receipt"
    PAYMENT = "Payment"
    JOURNAL = "Journal"
    CONTRA = "Contra"

class LedgerTypes:
    INCOME = "Income"
    EXPENSE = "Expense" 
    ASSET = "Asset"
    LIABILITY = "Liability"
    CAPITAL = "Capital"

class BalanceTypes:
    DEBIT = "Debit"
    CREDIT = "Credit"

class UserRoles:
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

# Tax Constants
class TaxRates:
    GST_0 = 0.0
    GST_5 = 5.0
    GST_12 = 12.0
    GST_18 = 18.0
    GST_28 = 28.0

# Report Types
class ReportTypes:
    DAILY = "daily"
    MONTHLY = "monthly" 
    YEARLY = "yearly"
    PROFIT_LOSS = "profit_loss"
    BALANCE_SHEET = "balance_sheet"
    TRIAL_BALANCE = "trial_balance"

# File Formats
class FileFormats:
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    PRINT = "print"

# Default Values
class Defaults:
    COMPANY_NAME = "Your Company Name"
    CURRENCY = "₹"
    DATE_FORMAT = "%d-%m-%Y"
    DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
    PAGE_SIZE = "A4"
    
# Error Messages
class ErrorMessages:
    INVALID_LOGIN = "Invalid username or password"
    USER_EXISTS = "Username already exists"
    LEDGER_EXISTS = "Ledger name already exists"
    ITEM_EXISTS = "Item code already exists"
    REQUIRED_FIELD = "This field is required"
    INVALID_AMOUNT = "Invalid amount"
    INVALID_DATE = "Invalid date format"
    DEBIT_CREDIT_MISMATCH = "Debit and Credit totals must be equal"

# Success Messages  
class SuccessMessages:
    LOGIN_SUCCESS = "Login successful"
    USER_CREATED = "User created successfully"
    LEDGER_CREATED = "Ledger created successfully"
    VOUCHER_CREATED = "Voucher created successfully"
    ITEM_CREATED = "Item created successfully"
    DATA_SAVED = "Data saved successfully"
    REPORT_GENERATED = "Report generated successfully"

# Table Names
class TableNames:
    USERS = "users"
    COMPANY = "company"
    LEDGERS = "ledgers"
    LEDGER_GROUPS = "ledger_groups"
    VOUCHERS = "vouchers"
    VOUCHER_ITEMS = "voucher_items"
    VOUCHER_TYPES = "voucher_types"
    INVENTORY_ITEMS = "inventory_items"
    SYSTEM_LOGS = "system_logs"

# Column Widths for Reports
class ColumnWidths:
    DATE = 80
    PARTICULARS = 200
    VOUCHER_NO = 100
    DEBIT = 100
    CREDIT = 100
    BALANCE = 100

# Print Margins (in points)
class PrintMargins:
    TOP = 72
    BOTTOM = 72
    LEFT = 72
    RIGHT = 72

# Font Sizes
class FontSizes:
    TITLE = 16
    HEADING = 12
    NORMAL = 10
    SMALL = 8