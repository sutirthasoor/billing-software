import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from config import Config
from assets.styles.theme import theme
from controllers.voucher_controller import VoucherController
from controllers.ledger_controller import LedgerController
from controllers.report_controller import ReportController
from views.widgets.chart_widget import ChartWidget, SparklineChart

class Dashboard:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.voucher_controller = VoucherController()
        self.ledger_controller = LedgerController()
        self.report_controller = ReportController()
        
        self.setup_ui()
        self.initialize_variables()  # Add this line
        self.load_dashboard_data()
    
    def setup_ui(self):
        # Main container with scrollbar
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(container, bg=Config.THEME['primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Modern.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Header
        header_frame = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        welcome_text = f"Welcome back, {self.user.full_name}!"
        ttk.Label(header_frame, text=welcome_text, 
                 style='Title.TLabel', font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        
        date_text = datetime.now().strftime("%A, %d %B %Y")
        ttk.Label(header_frame, text=date_text,
                 style='Normal.TLabel', foreground=Config.THEME['text_secondary']).pack(anchor='w')
        
        # Quick Stats Row
        self.setup_quick_stats()
        
        # Charts and Recent Activity Row
        self.setup_charts_and_activity()
        
        # Bottom row with additional widgets
        self.setup_bottom_row()
    
    def setup_quick_stats(self):
        """Setup quick statistics cards"""
        stats_frame = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Stats cards data
        self.stats_data = [
            {
                "title": "Today's Sales",
                "value": "0.00",
                "color": Config.THEME['success'],
                "icon": "💰",
                "trend": "↑ 12%"
            },
            {
                "title": "Today's Purchases", 
                "value": "0.00",
                "color": Config.THEME['danger'],
                "icon": "🛒",
                "trend": "↑ 8%"
            },
            {
                "title": "Total Ledgers",
                "value": "0",
                "color": Config.THEME['accent'],
                "icon": "📒",
                "trend": "↔"
            },
            {
                "title": "Pending Tasks",
                "value": "0",
                "color": Config.THEME['warning'],
                "icon": "⏰",
                "trend": "↓ 3%"
            }
        ]
        
        self.stat_cards = []
        for i, stat in enumerate(self.stats_data):
            card = self.create_stat_card(stats_frame, stat, i)
            self.stat_cards.append(card)
    
    def create_stat_card(self, parent, stat_data, index):
        """Create a single stat card"""
        card = theme.create_card(parent)
        card.grid(row=0, column=index, padx=5, pady=5, sticky='ew')
        parent.columnconfigure(index, weight=1)
        
        # Card content
        content_frame = ttk.Frame(card, style='Modern.TFrame')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Top row: Icon and trend
        top_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        top_frame.pack(fill='x')
        
        # Icon
        ttk.Label(top_frame, text=stat_data['icon'], 
                 font=('Segoe UI', 24)).pack(side='left')
        
        # Trend indicator
        trend_color = Config.THEME['success'] if '↑' in stat_data['trend'] else Config.THEME['danger'] if '↓' in stat_data['trend'] else Config.THEME['text_secondary']
        ttk.Label(top_frame, text=stat_data['trend'], 
                 style='Small.TLabel', foreground=trend_color).pack(side='right')
        
        # Value
        ttk.Label(content_frame, text=stat_data['value'], 
                 style='Title.TLabel', font=('Segoe UI', 24, 'bold'),
                 foreground=stat_data['color']).pack(anchor='w', pady=(5, 0))
        
        # Title
        ttk.Label(content_frame, text=stat_data['title'],
                 style='Normal.TLabel', foreground=Config.THEME['text_secondary']).pack(anchor='w')
        
        return card
    
    def setup_charts_and_activity(self):
        """Setup charts and recent activity section"""
        main_content = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        main_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - Charts (70% width)
        left_frame = ttk.Frame(main_content, style='Modern.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right side - Recent Activity (30% width)
        right_frame = ttk.Frame(main_content, style='Modern.TFrame', width=400)
        right_frame.pack(side='right', fill='both', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Charts section
        self.setup_charts_section(left_frame)
        
        # Recent activity section
        self.setup_activity_section(right_frame)
    
    def setup_charts_section(self, parent):
        """Setup charts section"""
        # Monthly Summary Chart
        chart_card = theme.create_card(parent)
        chart_card.pack(fill='both', expand=True, pady=(0, 10))
        
        chart_header = ttk.Frame(chart_card, style='Modern.TFrame')
        chart_header.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(chart_header, text="Monthly Summary", style='Heading.TLabel').pack(side='left')
        
        # Chart period selector
        period_frame = ttk.Frame(chart_header, style='Modern.TFrame')
        period_frame.pack(side='right')
        
        # Don't create the variable here - it will be created in initialize_variables
        period_combo = ttk.Combobox(period_frame,
                                   values=["7d", "30d", "90d", "1y"],
                                   style='Modern.TCombobox', width=8)
        period_combo.pack(side='left', padx=(0, 5))
        period_combo.bind('<<ComboboxSelected>>', self.on_chart_period_change)
        self.period_combo = period_combo  # Store reference for later
        
        # Chart container
        chart_container = ttk.Frame(chart_card, style='Modern.TFrame', height=300)
        chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        chart_container.pack_propagate(False)
        
        # Initialize chart (placeholder for now)
        self.chart_placeholder = ttk.Frame(chart_container, style='Modern.TFrame')
        self.chart_placeholder.pack(fill='both', expand=True)
        
        ttk.Label(self.chart_placeholder, text="📊 Charts will be displayed here", 
                 style='Normal.TLabel', foreground=Config.THEME['text_secondary']).pack(expand=True)
        
        # Quick Actions
        actions_card = theme.create_card(parent)
        actions_card.pack(fill='x', pady=(0, 10))
        
        ttk.Label(actions_card, text="Quick Actions", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        actions_frame = ttk.Frame(actions_card, style='Modern.TFrame')
        actions_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        actions = [
            ("💰 Create Sales Voucher", self.create_sales_voucher),
            ("🛒 Create Purchase", self.create_purchase_voucher),
            ("📒 Add New Ledger", self.create_ledger),
            ("📈 Generate Report", self.generate_report)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_frame, text=text, style='Secondary.TButton',
                           command=command)
            btn.pack(fill='x', pady=2)
    
    def initialize_variables(self):
        """Initialize Tkinter variables after UI is fully set up"""
        if not hasattr(self, 'chart_period_var') or self.chart_period_var is None:
            self.chart_period_var = tk.StringVar(value="30d")
            # Update the combobox with the variable
            if hasattr(self, 'period_combo'):
                self.period_combo.configure(textvariable=self.chart_period_var)
    
    def setup_activity_section(self, parent):
        """Setup recent activity section"""
        # Recent Vouchers
        recent_card = theme.create_card(parent)
        recent_card.pack(fill='both', expand=True)
        
        recent_header = ttk.Frame(recent_card, style='Modern.TFrame')
        recent_header.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(recent_header, text="Recent Vouchers", style='Heading.TLabel').pack(side='left')
        
        refresh_btn = ttk.Button(recent_header, text="🔄", style='Secondary.TButton',
                               width=3, command=self.refresh_recent_vouchers)
        refresh_btn.pack(side='right')
        
        # Vouchers list container
        self.vouchers_container = ttk.Frame(recent_card, style='Modern.TFrame')
        self.vouchers_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # System Status
        status_card = theme.create_card(parent)
        status_card.pack(fill='x', pady=(10, 0))
        
        ttk.Label(status_card, text="System Status", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        status_frame = ttk.Frame(status_card, style='Modern.TFrame')
        status_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        self.status_items = [
            ("Database", "🟢 Connected"),
            ("Users Online", "👤 1"),
            ("Last Backup", "💾 Today"),
            ("Storage", "💿 85% Free")
        ]
        
        self.status_labels = {}
        for item, status in self.status_items:
            item_frame = ttk.Frame(status_frame, style='Modern.TFrame')
            item_frame.pack(fill='x', pady=2)
            
            ttk.Label(item_frame, text=item, style='Normal.TLabel').pack(side='left')
            status_label = ttk.Label(item_frame, text=status, style='Normal.TLabel',
                                   foreground=Config.THEME['text_secondary'])
            status_label.pack(side='right')
            self.status_labels[item] = status_label
    
    def setup_bottom_row(self):
        """Setup bottom row with additional widgets"""
        bottom_frame = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        # Left - Performance metrics
        metrics_card = theme.create_card(bottom_frame)
        metrics_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(metrics_card, text="Performance Metrics", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        metrics_content = ttk.Frame(metrics_card, style='Modern.TFrame')
        metrics_content.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Performance metrics would go here
        ttk.Label(metrics_content, text="Monthly growth charts and KPIs", 
                 style='Normal.TLabel', foreground=Config.THEME['text_secondary']).pack(expand=True)
        
        # Right - Quick Notes
        notes_card = theme.create_card(bottom_frame)
        notes_card.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        ttk.Label(notes_card, text="Quick Notes", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        notes_content = ttk.Frame(notes_card, style='Modern.TFrame')
        notes_content.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.notes_text = tk.Text(notes_content, height=4, width=30, font=Config.FONTS['small'],
                                 bg=Config.THEME['primary'], relief='solid', bd=1)
        self.notes_text.pack(fill='both', expand=True)
        self.notes_text.insert('1.0', "Add your quick notes here...")
        
        notes_btn_frame = ttk.Frame(notes_content, style='Modern.TFrame')
        notes_btn_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(notes_btn_frame, text="Save Note", style='Secondary.TButton',
                  command=self.save_note).pack(side='right')
    
    def load_dashboard_data(self):
        """Load all dashboard data"""
        try:
            # Load today's date
            today = datetime.now().date()
            
            # Get today's vouchers
            today_vouchers = self.voucher_controller.get_vouchers_by_date_range(today, today)
            
            # Calculate totals
            sales_total = sum(v.total_amount for v in today_vouchers if v.voucher_type == "Sales")
            purchase_total = sum(v.total_amount for v in today_vouchers if v.voucher_type == "Purchase")
            
            # Get total ledgers
            ledgers = self.ledger_controller.get_all_ledgers()
            
            # Update stats cards
            self.update_stat_card(0, f"{Config.CURRENCY} {sales_total:,.2f}")
            self.update_stat_card(1, f"{Config.CURRENCY} {purchase_total:,.2f}")
            self.update_stat_card(2, str(len(ledgers)))
            
            # Update recent vouchers
            self.update_recent_vouchers(today_vouchers[:5])  # Show last 5
            
            # Update system status
            self.update_system_status()
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            # Set default values on error
            self.update_stat_card(0, f"{Config.CURRENCY} 0.00")
            self.update_stat_card(1, f"{Config.CURRENCY} 0.00")
            self.update_stat_card(2, "0")
            self.update_stat_card(3, "0")
    
    def update_stat_card(self, index, value):
        """Update a specific stat card"""
        if 0 <= index < len(self.stat_cards):
            # This would update the card value
            # For now, we'll just store the value
            self.stats_data[index]['value'] = value
    
    def update_recent_vouchers(self, vouchers):
        """Update recent vouchers display"""
        # Clear existing vouchers
        for widget in self.vouchers_container.winfo_children():
            widget.destroy()
        
        if not vouchers:
            ttk.Label(self.vouchers_container, text="No recent vouchers",
                     style='Normal.TLabel', foreground=Config.THEME['text_secondary']).pack(expand=True)
            return
        
        for voucher in vouchers:
            voucher_frame = self.create_voucher_item(voucher)
            voucher_frame.pack(fill='x', pady=2)
    
    def create_voucher_item(self, voucher):
        """Create a single voucher item display"""
        frame = ttk.Frame(self.vouchers_container, style='Modern.TFrame')
        
        # Voucher icon based on type
        icons = {
            "Sales": "💰",
            "Purchase": "🛒", 
            "Receipt": "🧾",
            "Payment": "💳",
            "Journal": "📝"
        }
        
        icon = icons.get(voucher.voucher_type, "📄")
        
        # Left side: Icon and voucher info
        left_frame = ttk.Frame(frame, style='Modern.TFrame')
        left_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(left_frame, text=f"{icon} {voucher.voucher_number}", 
                 style='Small.TLabel').pack(anchor='w')
        ttk.Label(left_frame, text=voucher.voucher_type,
                 style='Small.TLabel', foreground=Config.THEME['text_secondary']).pack(anchor='w')
        
        # Right side: Amount
        right_frame = ttk.Frame(frame, style='Modern.TFrame')
        right_frame.pack(side='right')
        
        ttk.Label(right_frame, text=f"{Config.CURRENCY} {voucher.total_amount:,.2f}",
                 style='Small.TLabel', foreground=Config.THEME['accent']).pack(anchor='e')
        
        return frame
    
    def update_system_status(self):
        """Update system status indicators"""
        # This would check actual system status
        # For now, we'll use placeholder values
        pass
    
    def on_chart_period_change(self, event):
        """Handle chart period change"""
        period = self.chart_period_var.get()
        # This would reload chart data based on period
        print(f"Chart period changed to: {period}")
    
    def refresh_recent_vouchers(self):
        """Refresh recent vouchers"""
        self.load_dashboard_data()
    
    def create_sales_voucher(self):
        """Navigate to sales voucher creation"""
        # This would be handled by the main window navigation
        print("Navigate to sales voucher")
    
    def create_purchase_voucher(self):
        """Navigate to purchase voucher creation"""
        print("Navigate to purchase voucher")
    
    def create_ledger(self):
        """Navigate to ledger creation"""
        print("Navigate to ledger creation")
    
    def generate_report(self):
        """Navigate to report generation"""
        print("Navigate to report generation")
    
    def save_note(self):
        """Save quick note"""
        note_content = self.notes_text.get('1.0', 'end-1c')
        if note_content.strip():
            # In a real implementation, this would save to database
            print("Note saved:", note_content)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def refresh_dashboard(self):
        """Refresh all dashboard data"""
        self.load_dashboard_data()