import tkinter as tk
from tkinter import ttk, messagebox
from config import Config
from assets.styles.theme import theme
from controllers.ledger_controller import LedgerController
from .create_ledger import CreateLedgerView
from .ledger_report import LedgerReportView

class LedgerMainView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.ledger_controller = LedgerController()
        self.current_view = None
        
        self.setup_ui()
        self.load_ledgers()
    
    def setup_ui(self):
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Ledger Management", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Action buttons
        action_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        action_frame.pack(side='right')
        
        ttk.Button(action_frame, text="➕ Create Ledger", style='Success.TButton',
                  command=self.show_create_ledger).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="📊 View Report", style='Modern.TButton',
                  command=self.show_ledger_report).pack(side='left')
        
        # Search and filter
        filter_card = theme.create_card(container)
        filter_card.pack(fill='x', pady=(0, 10))
        
        filter_frame = ttk.Frame(filter_card, style='Modern.TFrame')
        filter_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(filter_frame, text="Search:", style='Normal.TLabel').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var,
                                     style='Modern.TEntry', width=30)
        self.search_entry.pack(side='left', padx=(10, 20))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Label(filter_frame, text="Group:", style='Normal.TLabel').pack(side='left')
        self.group_var = tk.StringVar(value="All Groups")
        self.group_combo = ttk.Combobox(filter_frame, textvariable=self.group_var,
                                       style='Modern.TCombobox', width=20)
        self.group_combo.pack(side='left', padx=(10, 0))
        self.group_combo.bind('<<ComboboxSelected>>', self.on_group_filter)
        
        # Ledgers table
        table_card = theme.create_card(container)
        table_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(table_card, text="All Ledgers", style='Heading.TLabel').pack(anchor='w', padx=15, pady=10)
        
        # Treeview for ledgers
        columns = ('name', 'group', 'balance', 'type', 'contact', 'status', 'actions')
        self.ledgers_tree = ttk.Treeview(table_card, columns=columns, show='headings', style='Modern.Treeview')
        
        self.ledgers_tree.heading('name', text='Ledger Name')
        self.ledgers_tree.heading('group', text='Group')
        self.ledgers_tree.heading('balance', text='Balance')
        self.ledgers_tree.heading('type', text='Balance Type')
        self.ledgers_tree.heading('contact', text='Contact')
        self.ledgers_tree.heading('status', text='Status')
        self.ledgers_tree.heading('actions', text='Actions')
        
        self.ledgers_tree.column('name', width=200)
        self.ledgers_tree.column('group', width=150)
        self.ledgers_tree.column('balance', width=120)
        self.ledgers_tree.column('type', width=100)
        self.ledgers_tree.column('contact', width=150)
        self.ledgers_tree.column('status', width=80)
        self.ledgers_tree.column('actions', width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_card, orient='vertical', command=self.ledgers_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_card, orient='horizontal', command=self.ledgers_tree.xview)
        self.ledgers_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.ledgers_tree.pack(side='top', fill='both', expand=True, padx=15, pady=(0, 5))
        h_scrollbar.pack(side='bottom', fill='x', padx=15)
        v_scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 25))
        
        # Bind double-click for editing
        self.ledgers_tree.bind('<Double-1>', self.on_ledger_double_click)
        self.ledgers_tree.bind('<Button-1>', self.on_ledger_click)
        
        # Statistics
        stats_card = theme.create_card(container)
        stats_card.pack(fill='x')
        
        stats_frame = ttk.Frame(stats_card, style='Modern.TFrame')
        stats_frame.pack(fill='x', padx=15, pady=10)
        
        self.total_ledgers_var = tk.StringVar(value="Total Ledgers: 0")
        self.active_ledgers_var = tk.StringVar(value="Active: 0")
        
        ttk.Label(stats_frame, textvariable=self.total_ledgers_var, 
                 style='Normal.TLabel').pack(side='left', padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.active_ledgers_var,
                 style='Normal.TLabel', foreground=Config.THEME['success']).pack(side='left')
    
    def load_ledgers(self):
        """Load all ledgers"""
        try:
            # Clear existing data
            for item in self.ledgers_tree.get_children():
                self.ledgers_tree.delete(item)
            
            # Get ledgers
            ledgers = self.ledger_controller.get_all_ledgers()
            
            # Update statistics
            total_ledgers = len(ledgers)
            active_ledgers = sum(1 for ledger in ledgers if ledger.is_active)
            
            self.total_ledgers_var.set(f"Total Ledgers: {total_ledgers}")
            self.active_ledgers_var.set(f"Active: {active_ledgers}")
            
            # Load groups for filter
            groups = set()
            for ledger in ledgers:
                group_name = getattr(ledger, 'group_name', 'Unknown')
                groups.add(group_name)
            
            self.group_combo['values'] = ['All Groups'] + sorted(list(groups))
            
            # Populate treeview
            for ledger in ledgers:
                status = "🟢 Active" if ledger.is_active else "🔴 Inactive"
                contact = ledger.contact_person or ledger.phone or "-"
                
                self.ledgers_tree.insert('', 'end', values=(
                    ledger.name,
                    getattr(ledger, 'group_name', 'Unknown'),
                    f"{Config.CURRENCY} {float(ledger.opening_balance):,.2f}",
                    ledger.balance_type,
                    contact,
                    status,
                    "📊 View | ✏️ Edit | 🗑️ Delete"
                ), tags=(ledger.id,))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledgers: {str(e)}")
    
    def on_search(self, event=None):
        """Filter ledgers based on search"""
        search_term = self.search_var.get().lower()
        
        for item in self.ledgers_tree.get_children():
            values = self.ledgers_tree.item(item)['values']
            ledger_name = values[0].lower()
            group_name = values[1].lower()
            
            if search_term in ledger_name or search_term in group_name:
                self.ledgers_tree.item(item, tags=('visible',))
            else:
                self.ledgers_tree.item(item, tags=('hidden',))
    
    def on_group_filter(self, event=None):
        """Filter ledgers by group"""
        selected_group = self.group_var.get()
        
        if selected_group == "All Groups":
            # Show all
            for item in self.ledgers_tree.get_children():
                self.ledgers_tree.item(item, tags=('visible',))
        else:
            # Filter by group
            for item in self.ledgers_tree.get_children():
                values = self.ledgers_tree.item(item)['values']
                group_name = values[1]
                
                if group_name == selected_group:
                    self.ledgers_tree.item(item, tags=('visible',))
                else:
                    self.ledgers_tree.item(item, tags=('hidden',))
    
    def on_ledger_click(self, event):
        """Handle ledger actions"""
        item = self.ledgers_tree.identify_row(event.y)
        column = self.ledgers_tree.identify_column(event.x)
        
        if item and column == '#7':  # Actions column
            # Get the clicked position to determine which action was clicked
            x, y = event.x, event.y
            bbox = self.ledgers_tree.bbox(item, column)
            
            if bbox:
                # Calculate which action was clicked based on text position
                actions_text = self.ledgers_tree.item(item)['values'][6]
                action_width = bbox[2] / 3  # Divide actions column into 3 equal parts
                
                if x < bbox[0] + action_width:
                    # View Report clicked
                    self.view_ledger_report(item)
                elif x < bbox[0] + 2 * action_width:
                    # Edit clicked
                    self.edit_ledger(item)
                else:
                    # Delete clicked
                    self.delete_ledger(item)
    
    def on_ledger_double_click(self, event):
        """Handle double-click on ledger"""
        item = self.ledgers_tree.identify_row(event.y)
        if item:
            self.view_ledger_report(item)
    
    def view_ledger_report(self, item):
        """View ledger report"""
        ledger_id = self.ledgers_tree.item(item)['tags'][0]
        ledger_name = self.ledgers_tree.item(item)['values'][0]
        
        # Clear current view and show ledger report
        self.clear_current_view()
        self.current_view = LedgerReportView(self.parent, self.user, ledger_id, ledger_name)
    
    def edit_ledger(self, item):
        """Edit ledger"""
        ledger_id = self.ledgers_tree.item(item)['tags'][0]
        ledger_name = self.ledgers_tree.item(item)['values'][0]
        
        # For now, show message. In full implementation, this would open edit dialog
        messagebox.showinfo("Edit Ledger", f"Edit functionality for '{ledger_name}' would open here")
    
    def delete_ledger(self, item):
        """Delete ledger"""
        ledger_id = self.ledgers_tree.item(item)['tags'][0]
        ledger_name = self.ledgers_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete ledger '{ledger_name}'?\n\nThis action cannot be undone."):
            # Here you would call the controller to delete the ledger
            messagebox.showinfo("Delete", f"Ledger '{ledger_name}' would be deleted in full implementation")
            # After deletion, reload ledgers
            self.load_ledgers()
    
    def show_create_ledger(self):
        """Show create ledger view"""
        self.clear_current_view()
        self.current_view = CreateLedgerView(self.parent, self.user, self)
    
    def show_ledger_report(self):
        """Show ledger report view"""
        self.clear_current_view()
        self.current_view = LedgerReportView(self.parent, self.user)
    
    def clear_current_view(self):
        """Clear current view"""
        if self.current_view:
            # Clear the parent frame
            for widget in self.parent.winfo_children():
                widget.destroy()
            self.current_view = None
    
    def refresh_ledgers(self):
        """Refresh ledgers list"""
        self.load_ledgers()